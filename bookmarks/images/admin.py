from django.contrib import admin
from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Image model.
    """

    list_display = ["title", "slug", "image", "created"]
    list_filter = ["created"]
