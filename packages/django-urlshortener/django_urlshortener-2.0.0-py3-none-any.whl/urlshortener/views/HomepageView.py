from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.contrib.messages.views import SuccessMessageMixin
from urlshortener.modelforms import URLOnlyShortenerModelForm


""" Homepage Template view """
class HomepageTemplateView(TemplateView):
    template_name = "djangoadmin/urlshortener/homepage_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = URLOnlyShortenerModelForm()
        return context


""" Homepage Form view. """
class HomepageFormView(SuccessMessageMixin, FormView):
    template_name = "djangoadmin/urlshortener/homepage_view.html"
    form_class = URLOnlyShortenerModelForm
    success_url = reverse_lazy("homepage")
    success_message = None

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.author = self.request.user
        form.save()
        self.success_message = form.instance.slug
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return(f"https://{self.request.headers['Host']}/{self.success_message}")


""" Homepage view configurations. """
class HomepageView(View):
    def get(self, request, *args, **kwargs):
        view = HomepageTemplateView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = HomepageFormView.as_view()
        return view(request, *args, **kwargs)