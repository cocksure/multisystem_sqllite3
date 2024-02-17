from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import ChatRoom, ChatMessage
from .serializers import ChatRoomSerializer, ChatMessageSerializer


class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]


class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        sender = self.request.user
        timestamp = timezone.now()
        room = None
        if not sender.is_staff:
            if not sender.chat_rooms.exists():
                room = ChatRoom.objects.create(name=f"Room for {sender.username}")
                sender.chat_rooms.add(room)
            else:
                room = sender.chat_rooms.first()
        serializer.save(sender=sender, timestamp=timestamp, room=room)
