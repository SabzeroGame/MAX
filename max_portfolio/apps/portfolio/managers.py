from django.db import models


class PublishedProjectQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)


class PublishedProjectManager(models.Manager):
    def get_queryset(self):
        return PublishedProjectQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()