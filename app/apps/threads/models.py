from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ThreadManager(models.Manager):
    def create_thread(self, *, content: str, **kwargs):
        thread = super().create(**kwargs)
        ThreadMessage.objects.create_text_message(
            thread=thread,
            content=content,
            author=thread.owner,
            is_initial_thread_message=True,
        )
        return thread


class Thread(models.Model):
    class Meta:
        ordering = ["-timestamp"]

    timestamp = models.DateTimeField(
        auto_now_add=True,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="threads",
    )

    objects = ThreadManager()


class ThreadMessageManager(models.Manager):
    def create_text_message(self, **kwargs) -> ThreadMessage:
        message = ThreadMessage.objects.create(message_type="text", **kwargs)
        return message


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
        User,
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
    is_initial_thread_message = models.BooleanField(
        default=False,
    )

    objects = ThreadMessageManager()


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
