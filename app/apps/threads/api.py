from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from . import models, serializers


class ThreadListCreateAPIView(ListCreateAPIView):
    queryset = models.Thread.objects
    serializer_class = serializers.ThreadSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ThreadMessageRetrieveAPIView(RetrieveAPIView):
    queryset = models.ThreadMessage.objects
    serializer_class = serializers.ThreadMessageSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self):
        user_id = self.kwargs.get("user_id")
        thread_id = self.kwargs.get("thread_id")
        thread_message_id = self.kwargs.get("thread_message_id")

        filter_ = {
            "id": thread_message_id,
            "thread__id": thread_id,
            "thread__owner__id": user_id,
        }

        return get_object_or_404(models.ThreadMessage.objects, **filter_)
