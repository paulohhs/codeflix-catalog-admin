from django.contrib import admin

from src.django_project.video_app.models import (
    Video,
    AudioVideoMedia,
    ImageMedia,
)


class VideoAdmin(admin.ModelAdmin):
    pass


class AudioVideoAdmin(admin.ModelAdmin):
    pass


class ImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Video, VideoAdmin)
admin.site.register(AudioVideoMedia, AudioVideoAdmin)
admin.site.register(ImageMedia, ImageAdmin)
