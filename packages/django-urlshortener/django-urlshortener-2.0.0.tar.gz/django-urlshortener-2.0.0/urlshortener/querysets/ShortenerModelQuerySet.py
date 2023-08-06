from django.db.models import QuerySet


class ShortenerModelQuerySet(QuerySet):
    def active(self):
        return self.filter(status="ACTIVE")

    def author(self, user):
        return self.active().filter(author=user)