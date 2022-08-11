from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField()

    class Meta:
        model = Room
        exclude = ('room_user', )

    