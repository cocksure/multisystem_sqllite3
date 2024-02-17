from apps.users.serializers import CustomUserSerializer
from apps.chat.models import ChatMessage, ChatRoom
from rest_framework.serializers import ModelSerializer


class ChatMessageSerializer(ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'room', 'sender', 'message', 'timestamp']


class ChatRoomSerializer(ModelSerializer):
    users = CustomUserSerializer(many=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'users']
