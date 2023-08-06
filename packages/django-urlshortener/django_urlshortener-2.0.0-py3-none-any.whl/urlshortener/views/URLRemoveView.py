from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from djangotools.mixins import OnlyAuthorAccess
from urlshortener.models import ShortenerModel


class URLRemoveView(LoginRequiredMixin, OnlyAuthorAccess, View):
    model = ShortenerModel

    def get(self, request, *args, **kwargs):
        url_object = get_object_or_404(self.model, slug=self.kwargs['shortcode'])
        url_object.author = None
        url_object.save()
        return redirect("shortener:url_list_dashboard")