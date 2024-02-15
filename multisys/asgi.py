import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import apps.depo.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multisys.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            apps.depo.routing.websocket_urlpatterns
        )
    ),
})
