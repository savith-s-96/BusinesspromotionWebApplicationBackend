import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Locito.settings')

from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import LocitoApi.websocketroutes

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            LocitoApi.websocketroutes.websocket_urlpatterns
        )
    ),
})
