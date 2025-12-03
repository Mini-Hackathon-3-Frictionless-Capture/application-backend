from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.threads.models import ThreadMessage

from . import models


@receiver(post_save, sender=models.Note)
def create_bot_message_on_note_creation(instance: models.Note, created: bool, **kwargs):
    if not created:
        return
    ThreadMessage.objects.create_text_message(
        content=(
            f"Geschafft! Ich habe dir eine Note erstellt. "
            f"Diese findest du hier: :NOTE-{instance.id}:"
        ),
        is_bot_message=True,
        thread=instance.thread,
    )
