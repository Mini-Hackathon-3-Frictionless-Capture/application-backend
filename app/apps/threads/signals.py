from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models


@receiver(post_save, sender=models.ThreadMessage)
def create_initial_system_prompt(instance: models.ThreadMessage, created: bool, **kwargs):
    if not created or not instance.is_initial_thread_message:
        return
    models.ThreadMessage.objects.create_text_message(
        content=(
            "Vielen Dank für deine Nachricht! "
            "Ich werde den Inhalt jetzt in deinem Knowledge Capture system einsortieren."
        ),
        is_bot_message=True,
        thread=instance.thread,
    )
