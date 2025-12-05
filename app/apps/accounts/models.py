from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Usage(models.Model):
    class Meta:
        ordering = ("-date",)
        unique_together = ("user", "date")

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="usage",
    )
    date = models.DateField(
        auto_now_add=True,
    )
    max_usage = models.PositiveIntegerField(
        default=50,
    )
    use_fake_data = models.BooleanField(
        default=True,
    )

    @property
    def current_usage(self):
        return self.user.threads.count()
