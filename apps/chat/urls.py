from django.urls import path
from .views import ChatMessageListCreateAPIView, ChatRoomListCreateApiView, send_test_message_view

urlpatterns = [
    path('', ChatMessageListCreateAPIView.as_view(), name='chatmessage'),
    path('chatroom/', ChatRoomListCreateApiView.as_view(), name='chatmessage'),
    path('send_test_message/', send_test_message_view, name='send_test_message'),
]
