from django.urls import reverse_lazy
from django.views.generic import UpdateView
from djangotools.mixins import OnlyAuthorAccess
from django.contrib.auth.mixins import LoginRequiredMixin
from urlshortener.models import ShortenerModel
from urlshortener.modelforms import ShortenerModelForm


class URLUpdateView(LoginRequiredMixin, OnlyAuthorAccess, UpdateView):
    template_name = "djangoadmin/urlshortener/url_create_view.html"
    model = ShortenerModel
    form_class = ShortenerModelForm
    slug_url_kwarg = "shortcode"
    success_url = reverse_lazy("shortener:url_list_dashboard")

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = "ACTIVE"
        form.save()
        return super().form_valid(form)