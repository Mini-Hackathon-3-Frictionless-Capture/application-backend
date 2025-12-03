from django.urls import path

from . import api

urlpatterns = [
    path(
        "",
        api.TaskListAPIView.as_view(),
        name="tasks__tasks",
    ),
]
