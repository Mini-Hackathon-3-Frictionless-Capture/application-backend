from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/accounts/", include("apps.accounts.urls")),
    path("api/threads/", include("apps.threads.urls")),
    path("api/notes/", include("apps.notes.urls")),
    path("api/tasks/", include("apps.tasks.urls")),
]
