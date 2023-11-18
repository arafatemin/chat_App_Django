from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # room sayfasindan js ile gelen url bilgisi
    re_path(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer.as_asgi()),
]