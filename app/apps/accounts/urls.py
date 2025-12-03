from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import api

urlpatterns = [
    path("auth/token", obtain_auth_token),
    path(
        "me",
        api.MeAPIView.as_view(),
        name="accounts__me",
    ),
]
