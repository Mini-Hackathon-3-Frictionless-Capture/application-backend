from django.urls import path

from . import api

urlpatterns = [
    path(
        "",
        api.ThreadListCreateAPIView.as_view(),
        name="threads__threads",
    ),
]
