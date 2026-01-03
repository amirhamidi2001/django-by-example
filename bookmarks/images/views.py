from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ImageCreateForm


@login_required
def image_create(request):
    """
    View responsible for creating a new Image instance.
    """
    if request.method == "POST":
        form = ImageCreateForm(data=request.POST)

        if form.is_valid():
            new_image = form.save(commit=False)

            # Associate image with the current user
            new_image.user = request.user
            new_image.save()

            messages.success(request, "Image added successfully.")
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)

    return render(
        request,
        "images/image/create.html",
        {
            "section": "images",
            "form": form,
        },
    )
