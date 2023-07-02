from .models import *
from rest_framework.serializers import ModelSerializer

class UserSerializer(ModelSerializer):
    class Meta:
        model=User
        fields="__all__"

class ProfileSerializer(ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model=Profile
        fields = "__all__"


class ChatRoomSerializer(ModelSerializer):
    class Meta:
        model=ChatRoom
        fields = "__all__"


class ChatMessageSerializer(ModelSerializer):
    class Meta:
        model=ChatMessage
        fields = "__all__"


class ChatNotificationSerializer(ModelSerializer):
    class Meta:
        model=ChatNotification
        fields = "__all__"

