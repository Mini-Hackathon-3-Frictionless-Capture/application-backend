from django.conf import settings
from django.db import models


class Thread(models.Model):
    timestamp = models.DateTimeField(
        auto_now_add=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="threads",
    )

    class Meta:
        ordering = ["-timestamp"]


class ThreadMessage(models.Model):
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
    )
    content = models.TextField(
        blank=True,
    )
    is_bot_message = models.BooleanField(
        default=False,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="thread_messages",
        null=True,
    )

    class Meta:
        ordering = ["-timestamp"]


class ThreadMessageImageAttachment(models.Model):
    thread = models.ForeignKey(
        ThreadMessage,
        on_delete=models.CASCADE,
        related_name="image_attachments",
    )
    image = models.ImageField(
        upload_to="threads/images/",
    )


class ThreadMessageAudioAttachment(models.Model):
    thread = models.ForeignKey(
        ThreadMessage,
        on_delete=models.CASCADE,
        related_name="audio_attachments",
    )
    audio = models.FileField(
        upload_to="threads/audio/",
    )
