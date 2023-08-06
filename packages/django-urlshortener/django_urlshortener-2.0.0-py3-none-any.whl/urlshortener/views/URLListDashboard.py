from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from urlshortener.models import ShortenerModel


class URLListDashboard(LoginRequiredMixin, ListView):
    template_name = "djangoadmin/urlshortener/url_list_dashboard.html"
    context_object_name = "url_list"

    def get_queryset(self):
        return ShortenerModel.objects.author(self.request.user)