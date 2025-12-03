from rest_framework import serializers

from . import models


class ThreadMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ThreadMessage
        fields = "__all__"


class ThreadSerializer(serializers.ModelSerializer):
    content = serializers.CharField(write_only=True)
    messages = ThreadMessageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Thread
        fields = (
            "id",
            "timestamp",
            "content",
            "messages",
        )

    def create(self, validated_data: dict) -> models.Thread:
        user = validated_data.pop("user")
        return models.Thread.objects.create_thread(
            owner=user,
            content=validated_data["content"],
        )
