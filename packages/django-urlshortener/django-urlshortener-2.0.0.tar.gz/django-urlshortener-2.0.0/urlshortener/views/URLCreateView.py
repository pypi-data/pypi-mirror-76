from django.views.generic import CreateView
from urlshortener.models import ShortenerModel
from urlshortener.modelforms import ShortenerModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class URLCreateView(LoginRequiredMixin, CreateView):
    template_name = "djangoadmin/urlshortener/url_create_view.html"
    model = ShortenerModel
    form_class = ShortenerModelForm
    success_url = reverse_lazy("shortener:url_list_dashboard")

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = "ACTIVE"
        form.save()
        return super().form_valid(form)