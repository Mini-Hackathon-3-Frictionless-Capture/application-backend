from django.urls import path

from . import api

urlpatterns = [
    path(
        "",
        api.NoteListAPIView.as_view(),
        name="notes__notes",
    ),
    path(
        "user/<int:user_id>/thread/<int:thread_id>",
        api.NoteCreateAPIView.as_view(),
        name="notes__user__thread",
    ),
]
