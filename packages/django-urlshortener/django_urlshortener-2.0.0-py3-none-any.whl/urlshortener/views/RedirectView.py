from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from urlshortener.models import ShortenerModel


""" Redirect View. """
def RedirectView(request, slug):
    data = get_object_or_404(ShortenerModel, slug=slug)
    return redirect(data.url)