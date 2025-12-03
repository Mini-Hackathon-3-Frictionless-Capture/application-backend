from django.contrib import admin

from . import models


@admin.register(models.Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__", "owner", "thread", "timestamp")
