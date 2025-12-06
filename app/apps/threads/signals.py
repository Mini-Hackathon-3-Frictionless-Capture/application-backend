import random

import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from faker import Faker

from . import models

fake = Faker(["de_DE"])


def get_airflow_jwt_token() -> str:
    response = requests.post(
        url=f"{settings.AIRFLOW['host']}/auth/token",
        json={
            "username": settings.AIRFLOW["username"],
            "password": settings.AIRFLOW["password"],
        },
    )
    response.raise_for_status()
    return response.json()["access_token"]


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
def generate_classification(instance: models.ThreadMessage, created: bool, **kwargs):
    if not created or not instance.is_initial_thread_message:
        return

    today = now().date()
    filter_ = {
        "date__year": today.year,
        "date__month": today.month,
    }
    usage = instance.thread.owner.usage.filter(**filter_)
    if not usage.exists():
        models.ThreadMessage.objects.create_text_message(
            content=(
                "Leider ist dein Account nicht für die Nutzung dieser Anwendung freigeschaltet. "
                "Bitte wende dich an einen Administrator."
            ),
            is_bot_message=True,
            thread=instance.thread,
        )
        return

    usage = usage.first()

    if usage.use_fake_data:
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

    elif usage.max_usage < usage.current_usage:
        models.ThreadMessage.objects.create_text_message(
            content=(
                "Leider sind deine Credits für diesen Monat bereits aufgebraucht. Bitte warte auf "
                "den kommenden Monat oder wende dich an einen Administrator."
            ),
            is_bot_message=True,
            thread=instance.thread,
        )
        return

    else:
        try:
            access_token = get_airflow_jwt_token()
            response = requests.post(
                url=f"{settings.AIRFLOW['host']}/api/v2/dags/automation/dagRuns",
                json={
                    "logical_date": now().isoformat(),
                    "conf": {
                        "payload": {
                            "user_id": instance.thread.owner.id,
                            "thread_id": instance.thread.id,
                            "thread_message_id": instance.id,
                        },
                    },
                },
                headers={
                    "Authorization": f"Bearer {access_token}",
                },
            )
            response.raise_for_status()
            models.ThreadMessage.objects.create_text_message(
                content=(
                    "Deine Nachricht wurde jetzt an die KI zur Verarbeitung gegeben. "
                    "Das entwicklerteam war faul und hat keine Websockets implementiert. "
                    "Bitte lade diese Seite alle par Sekunden neu um Up2Date zu bleiben <3."
                ),
                is_bot_message=True,
                thread=instance.thread,
            )

        except requests.exceptions.HTTPError:
            models.ThreadMessage.objects.create_text_message(
                content=("Huch! Das Entwicklerteam war inkompetent! Da ist was schief gegangen."),
                is_bot_message=True,
                thread=instance.thread,
            )
