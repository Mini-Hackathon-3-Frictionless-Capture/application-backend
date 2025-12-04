from django.urls import path

from . import api

urlpatterns = [
    path(
        "",
        api.TaskListAPIView.as_view(),
        name="tasks__tasks",
    ),
    path(
        "user/<int:user_id>/thread/<int:thread_id>",
        api.TaskCreateAPIView.as_view(),
        name="tasks__user__thread",
    ),
]
