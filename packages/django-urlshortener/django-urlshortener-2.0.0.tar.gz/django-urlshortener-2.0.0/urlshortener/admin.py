from django.contrib import admin
from urlshortener.models import ShortenerModel
from urlshortener.modeladmins import ShortenerModelAdmin


# Register your models here.
admin.site.register(ShortenerModel, ShortenerModelAdmin)
