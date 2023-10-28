# Posting contents from other websites

# Implementing request library and overriding
# the save() of a model form 
from django.core.files.base import ContentFile
from django.utils.text import slugify
import requests  # for a modelform

from django import forms

from .models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        widgets = {
            'url': forms.HiddenInput,
        }

    # cleaning the form fields
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError("The given URL doesn't " \
                                        "match a valid image extensions.")
        return url
    
    # Using the Request library (pip install requests==2.28.1)
    # to retrieve the image by its url, so we'll override the
    # save()
    def save(self, force_insert=False, force_update=False,
             commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'
        # download image from the given URL
        response = requests.get(image_url)
        image.image.save(image_name,
                         ContentFile(response.content),
                         save=False)
        if commit:
            image.save()
        return image

