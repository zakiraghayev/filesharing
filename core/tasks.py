from celery import shared_task
from django.shortcuts import get_object_or_404

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import FileContainer

@shared_task
def remove(id):
    """remove file after a week."""
    file = get_object_or_404( FileContainer, pk=id )
    file.delete()
    print("File has been deleted.", file.name)


@receiver(post_save, sender=FileContainer)
def update_stock(sender, instance, created, **kwargs):
    # print("Signals recieved.", instance, created, kwargs)
    if created:
        remove.apply_async(args=[instance.id], countdown=7*24*3600)