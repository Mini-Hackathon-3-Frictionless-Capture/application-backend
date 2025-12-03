from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from . import models, serializers


class NoteListAPIView(ListAPIView):
    queryset = models.Note.objects.all()
    serializer_class = serializers.NoteSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
