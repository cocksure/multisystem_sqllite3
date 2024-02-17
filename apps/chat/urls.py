from rest_framework.routers import DefaultRouter
from .views import ChatRoomViewSet, ChatMessageViewSet

router = DefaultRouter()
router.register(r'chatrooms', ChatRoomViewSet)
router.register(r'chatmessages', ChatMessageViewSet)

urlpatterns = router.urls
