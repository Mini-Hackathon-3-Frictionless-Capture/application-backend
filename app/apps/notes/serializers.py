from rest_framework import serializers

from . import models


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Note
        fields = "__all__"
        read_only_fields = ("thread", "owner")

    def create(self, validated_data):
        return models.Note.objects.create(**validated_data)
