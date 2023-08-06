from django import forms
from django.forms import ModelForm
from urlshortener.models import ShortenerModel


class URLOnlyShortenerModelForm(ModelForm):
    class Meta:
        model   = ShortenerModel
        fields  = ["url", "author"]

        widgets = {
            "url": forms.URLInput(attrs={'class': 'form-control rounded-0', 'placeholder': 'Shorten your link.'})
        }