import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message


class ChatConsumer(WebsocketConsumer):
    # Baglanti basladiginda yapilacaklar
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        print("baglandi")
        # room groub'a katilma
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()


    # Web socket basglantisi kapandi
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )



    # istemciden mesaj geldiginde yapilacaklar
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        what_is_it = text_data_json["what_is_it"]
        user = self.scope["user"] # bilgiler alindi
        m = Message.objects.create(content=message, user=user, room_id=self.room_name, what_is_it=what_is_it)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user": user.username,
                "what_is_it": what_is_it,
                "created_date": str(m.created_date.hour) + ":" + str(m.created_date.minute) + ":" + str(m.created_date.second)
            }  # chat mesaj'a gonderildi
        )



    # Django tarafindan istemciye mesaj gonderir
    def chat_message(self, event):
        message = event["message"]
        user = event["user"] # bilgiler alindi
        created_date = event["created_date"] # bilgiler alindi
        what_is_it = event["what_is_it"]
        # Send message to WebSocket
        self.send(text_data=json.dumps(
            {
                "message": message,
                "what_is_it": what_is_it,
                "user": user,
                "created_date": created_date
             })) # js'e gonderildi