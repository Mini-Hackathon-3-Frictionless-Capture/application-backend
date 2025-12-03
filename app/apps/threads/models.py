from django.conf import settings
from django.db import models


class Thread(models.Model):
    class Meta:
        ordering = ["-timestamp"]

    timestamp = models.DateTimeField(
        auto_now_add=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="threads",
    )


class ThreadMessage(models.Model):
    class Meta:
        ordering = ["-timestamp"]

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
    message_type = models.CharField(
        choices=[
            ("text", "text"),
            ("image", "image"),
            ("audio", "audio"),
        ],
        default="text",
        max_length=20,
    )


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
