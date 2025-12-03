import random

from django.db.models.signals import post_save
from django.dispatch import receiver
from faker import Faker

from . import models

fake = Faker(["de_DE"])


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


@receiver(post_save, sender=models.ThreadMessage)
def tmp_generate_classification(instance: models.ThreadMessage, created: bool, **kwargs):
    if not created or not instance.is_initial_thread_message:
        return

    from apps.notes.models import Note  # noqa
    from apps.tasks.models import Task  # noqa

    possible_actions = ["note", "task"]

    choice = random.choice(possible_actions)

    if choice == "note":
        Note.objects.create(
            title=fake.sentence(nb_words=6, variable_nb_words=True).rstrip("."),
            content=fake.text(),
            owner=instance.thread.owner,
            thread=instance.thread,
            meta_data={},
        )
    else:
        Task.objects.create(
            title=fake.sentence(nb_words=6, variable_nb_words=True).rstrip("."),
            content=fake.text(),
            owner=instance.thread.owner,
            thread=instance.thread,
            meta_data={},
        )
