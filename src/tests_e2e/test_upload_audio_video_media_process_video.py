import pytest
import json
import pika
import time

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db(transaction=True)
class TestUploadAudioVideoMediaProcessVideo:
    def send_message_to_rabbitmq(self, video_id: str) -> None:
        QUEUE = "videos.converted"
        HOST = "localhost"
        PORT = 5672

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=HOST,
                port=PORT,
            ),
        )
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE)

        message = {
            "error": "",
            "video": {
                "resource_id": video_id,
                "encoded_video_folder": "/path/to/encoded/video",
            },
            "status": "COMPLETED",
        }
        channel.basic_publish(exchange='', routing_key=QUEUE, body=json.dumps(message))

        print("Sent message")
        connection.close()

    def test_upload_audio_video_media_process_video(self):
        api_client = APIClient()

        # Verifica que lista de categorias esta vazia
        list_response = api_client.get('/api/categories/')
        assert list_response.data["data"] == []

        # Criar uma categoria
        create_response = api_client.post(
            '/api/categories/',
            data={
                "name": "Movie",
                "description": "Movie description",
            }
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        created_category_id = create_response.data["id"]

        # Verifica que lista de generos esta vazia
        list_response = api_client.get('/api/genres/')
        assert list_response.data["data"] == []

        # Criar um genero com categoria
        create_response = api_client.post(
            '/api/genres/',
            data={
                "name": "Comedy",
                "categories": [str(created_category_id)],
            }
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        created_genre_id = create_response.data["id"]

        # Verifica que lista de cast members esta vazia
        list_response = api_client.get('/api/cast_members/')
        assert list_response.data["data"] == []

        # Criar um cast member
        create_response = api_client.post(
            '/api/cast_members/',
            data={
                "name": "Actor Member",
                "type": "ACTOR",
            }
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        created_cast_member_id = create_response.data["id"]

        # Confirma que não existe vídeos na listagem
        list_response = api_client.get("/api/videos/")
        assert list_response.status_code == status.HTTP_200_OK
        assert list_response.data["data"] == []

        # Cria um novo vídeo sem media
        create_response = api_client.post(
            "/api/videos/",
            data={
                "title": "title",
                "description": "description",
                "launch_year": 2019,
                "opened": True,
                "rating": "L",
                "duration": 1.00,
                "categories": [str(created_category_id)],
                "genres": [str(created_genre_id)],
                "cast_members": [str(created_cast_member_id)]
            },
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        assert create_response.data['id']

        created_video_id = create_response.data['id']

        # Faz upload de video_midia do video
        video_file_mock = SimpleUploadedFile(
            name="video.mp4",
            content=b"images/123123/video.mp4",
            content_type="video/mp4"
        )
        response = api_client.patch(
            f"/api/videos/{created_video_id}/",
            data={"video_file": video_file_mock},
            format="multipart",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        self.send_message_to_rabbitmq(f"{created_video_id}.VIDEO")
        time.sleep(10)

        # Confirma que o status do vídeo é COMPLETED
        list_response = api_client.get("/api/videos/")
        assert list_response.data["data"][0]["video"]
        assert list_response.data["data"][0]["video"]["status"] == "COMPLETED"
