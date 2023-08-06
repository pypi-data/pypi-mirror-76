from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from urlshortener.validators import shortcode_not_allowed
from urlshortener.extra import get_shortcode
from urlshortener.managers import ShortenerModelManager


# Create your models here.
class ShortenerModel(models.Model):

    STATUS_CHOICES = (
        ("ACTIVE", "active"),
        ("DEACTIVE", "deactive")
    )

    title       = models.CharField(max_length=60, null=True, blank=True)
    description = models.CharField(max_length=160, null=True, blank=True)
    image       = models.ImageField(null=True, blank=True)
    url         = models.URLField()
    slug        = models.CharField(max_length=5, unique=True)
    status      = models.CharField(max_length=8, choices=STATUS_CHOICES, default="active")
    author      = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at  = models.DateTimeField(auto_now=True)
    updated_at  = models.DateTimeField(auto_now_add=True)

    objects     = ShortenerModelManager()

    def get_absolute_detail_url(self, **kwargs):
        return reverse("shortener:url_detail_dashboard", kwargs={'shortcode': self.slug})

    def get_absolute_update_url(self, **kwargs):
        return reverse("shortener:url_update_view", kwargs={'shortcode': self.slug})

    def get_absolute_remove_url(self, **kwargs):
        return reverse("shortener:url_remove_view", kwargs={'shortcode': self.slug})

    def __str__(self):
        return f"{self.url}"

    def save(self, *args, **kwargs):
        if self.slug == None or self.slug == "":
            self.slug   = get_shortcode(5)
            self.status = "ACTIVE"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name        = "Shortener"
        verbose_name_plural = "Shorteners"
        ordering            = ["-pk"]