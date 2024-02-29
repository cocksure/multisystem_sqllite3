from django.utils.decorators import method_decorator
from django.utils import timezone
from rest_framework.generics import ListCreateAPIView

from .models import ChatRoom, ChatMessage
from .serializers import ChatRoomSerializer, ChatMessageSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from channels.layers import get_channel_layer
from django.views.decorators.cache import cache_page

from apps.shared.utils import CustomPagination


async def send_test_message_view(request):
    room_id = '1'
    chat_group_name = f'chat_{room_id}'
    channel_layer = get_channel_layer()

    await channel_layer.group_send(
        chat_group_name,
        {
            'type': 'chat.message',
            'message': 'Test message'
        }
    )

    return HttpResponse('Test message sent')


class ChatRoomListCreateApiView(ListCreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    pagination_class = CustomPagination


class ChatMessageListCreateAPIView(ListCreateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        return ChatMessage.objects.all()

    @method_decorator(cache_page(60))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

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
        else:
            room_id = self.request.data.get('room')
            if room_id:
                try:
                    room = ChatRoom.objects.get(id=room_id)
                except ChatRoom.DoesNotExist:
                    pass

        if room:
            serializer.save(sender=sender, timestamp=timestamp, room=room)
        else:
            return Response({"error": "Room not found"}, status=status.HTTP_400_BAD_REQUEST)
