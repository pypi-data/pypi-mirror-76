from django.db.models import Manager
from urlshortener.querysets import ShortenerModelQuerySet


class ShortenerModelManager(Manager):
    def get_queryset(self):
        return ShortenerModelQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def author(self, user):
        return self.get_queryset().author(user)