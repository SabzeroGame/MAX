from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Project


@receiver(post_save, sender=Project)
def clear_category_cache_on_project_update(sender, **kwargs):
    cache.delete("portfolio_categories_with_counts")