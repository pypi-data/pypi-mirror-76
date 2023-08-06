from django import forms
from django.forms import ModelForm
from urlshortener.models import ShortenerModel


class ShortenerModelForm(ModelForm):
    class Meta:
        model   = ShortenerModel
        fields  = ["title", "description", "image", "url", "slug"]

        labels = {
            "title": "Title",
            "description": "Description",
            "image": "Image",
            "url": "URL",
            "slug": "Shortcode"
        }

        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control rounded-0', 'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'type': 'text', 'rows': '3', 'class': 'form-control border-0 rounded-0', 'placeholder':'Description'}),
            "image": forms.FileInput(attrs={'type': 'file', 'class': 'custom-file-input rounded-0'}),
            "url": forms.URLInput(attrs={'class': 'form-control rounded-0', 'placeholder': 'Original URL.'}),
            "slug": forms.TextInput(attrs={'class': 'form-control rounded-0', 'placeholder': 'Shortcode'})
        }