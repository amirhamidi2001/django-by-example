import requests
from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify

from .models import Image


class ImageCreateForm(forms.ModelForm):
    """
    Form used to create an Image instance from an external URL.
    """

    class Meta:
        model = Image
        fields = ["title", "url", "description"]

        # Hide the URL field (typically populated via JavaScript)
        widgets = {
            "url": forms.HiddenInput(),
        }

    def clean_url(self):
        """
        Validate that the provided URL points to a supported image format.
        """
        url = self.cleaned_data["url"]
        valid_extensions = ["jpg", "jpeg", "png", "webp"]

        extension = url.rsplit(".", 1)[-1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError(
                "The provided URL does not point to a valid image format."
            )

        return url

    def save(self, commit=True):
        """
        Download the image from the provided URL and save it locally.
        """
        image = super().save(commit=False)

        image_url = self.cleaned_data["url"]
        name = slugify(image.title)
        extension = image_url.rsplit(".", 1)[-1].lower()
        image_name = f"{name}.{extension}"

        # Download image content
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()

        # Save image file without committing yet
        image.image.save(
            image_name,
            ContentFile(response.content),
            save=False,
        )

        if commit:
            image.save()

        return image
