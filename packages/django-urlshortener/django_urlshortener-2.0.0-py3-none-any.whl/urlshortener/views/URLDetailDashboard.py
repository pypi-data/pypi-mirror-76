from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from djangotools.mixins import OnlyAuthorAccess
from urlshortener.models import ShortenerModel


class URLDetailDashboard(LoginRequiredMixin, OnlyAuthorAccess, DetailView):
    template_name = "djangoadmin/urlshortener/url_detail_dashboard.html"
    model = ShortenerModel
    slug_url_kwarg = "shortcode"
    context_object_name = "url_object"