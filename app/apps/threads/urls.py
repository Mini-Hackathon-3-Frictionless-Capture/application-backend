from django.urls import path

from . import api

urlpatterns = [
    path(
        "",
        api.ThreadListCreateAPIView.as_view(),
        name="threads__threads",
    ),
    path(
        "user/<int:user_id>/thread/<int:thread_id>/message/<int:thread_message_id>",
        api.ThreadMessageRetrieveAPIView.as_view(),
        name="threads__user__thread__message",
    ),
]
