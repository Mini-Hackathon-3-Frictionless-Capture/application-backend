from django.contrib import admin

from . import models


class ThreadMessageInline(admin.TabularInline):
    model = models.ThreadMessage
    extra = 0


@admin.register(models.Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "timestamp")
    inlines = (ThreadMessageInline,)


class ThreadMessageImageAttachmentInline(admin.TabularInline):
    model = models.ThreadMessageImageAttachment
    extra = 0


class ThreadMessageAudioAttachmentInline(admin.TabularInline):
    model = models.ThreadMessageAudioAttachment
    extra = 0


@admin.register(models.ThreadMessage)
class ThreadMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "thread", "is_bot_message", "author", "message_type", "timestamp")
    list_filter = ("is_bot_message", "message_type")
    inlines = (ThreadMessageImageAttachmentInline, ThreadMessageAudioAttachmentInline)
