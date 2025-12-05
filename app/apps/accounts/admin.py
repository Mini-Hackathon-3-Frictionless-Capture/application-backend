from django.contrib import admin

from . import models


@admin.register(models.Usage)
class UsageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "date",
        "max_usage",
        "current_usage",
        "current_usage",
        "use_fake_data",
    )
    readonly_fields = (
        "max_usage",
        "current_usage",
        "use_fake_data",
    )
