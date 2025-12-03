from django.contrib.auth import get_user_model
from django.db import models

from apps.threads.models import Thread

User = get_user_model()


class Note(models.Model):
    class Meta:
        ordering = ("-timestamp",)

    title = models.CharField(
        max_length=1024,
    )
    content = models.TextField(
        blank=True,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notes",
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
    )
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
        related_name="notes",
    )
    meta_data = models.JSONField(
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        if len(self.title) > 60:
            return f"{self.title[:60]}..."
        return f"{self.title}"
