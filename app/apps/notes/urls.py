from django.urls import path

from . import api

urlpatterns = [
    path(
        "",
        api.NoteListAPIView.as_view(),
        name="notes__notes",
    ),
]
