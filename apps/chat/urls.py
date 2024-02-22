from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatRoomViewSet, ChatMessageViewSet, send_test_message_view

router = DefaultRouter()
router.register(r'chatrooms', ChatRoomViewSet)
router.register(r'chatmessages', ChatMessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('send_test_message/', send_test_message_view, name='send_test_message'),
]
