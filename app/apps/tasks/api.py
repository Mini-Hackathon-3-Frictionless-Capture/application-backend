from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from . import models, serializers


class TaskListAPIView(ListAPIView):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class TaskCreateAPIView(CreateAPIView):
    serializer_class = serializers.TaskSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        thread_id = self.kwargs.get("thread_id")
        owner_id = self.kwargs.get("user_id")

        filter_ = {
            "id": thread_id,
            "owner__id": owner_id,
        }

        thread = get_object_or_404(models.Thread, **filter_)
        serializer.save(thread=thread, owner=thread.owner)
