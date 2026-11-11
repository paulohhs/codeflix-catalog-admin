# codeflix-catalog-admin

Tecnologias:
- Python 3.14.4
- Django 6.1.2

Intalação das dependências:

`pip install -r requirements.txt`

Execução do servidor para testes:

`python manage.py runserver`

IMPORTANTE:

* Para executar o teste e2e do arquivo `src/tests_e2e/test_upload_audio_video_media_process_video.py` é necessário inicializar o server do rabbitmq e também o consumer. 
* Na inicialização do consumer também é necessário informar um `DB_NAME` para que o consumer consiga utilizar o mesmo banco do teste.

Comando para inicializar o server do rabbitmq: 

`docker run -d --hostname rabbitmq --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management`

Comando para inicializar o consumer para teste: 

`DB_NAME=$PWD/db_e2e.sqlite3 python manage.py startconsumer`