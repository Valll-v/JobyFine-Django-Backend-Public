    from django.urls import re_path

from chats.consumers import WSConsumer

websocket_urlpatterns = [
    re_path(r'^ws/', WSConsumer.as_asgi()),
]
