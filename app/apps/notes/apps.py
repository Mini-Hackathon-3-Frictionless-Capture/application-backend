from django.apps import AppConfig


class NotesConfig(AppConfig):
    name = "apps.notes"

    def ready(self):
        from . import signals  # noqa
