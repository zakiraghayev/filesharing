import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.shortcuts import get_object_or_404

from .models import FileContainer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "newfile_"+self.scope['url_route']['kwargs']['pk']
        self.context = {"pk":self.scope['url_route']['kwargs']['pk']}
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Send message to room group
        await self.save_comments(message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username':self.scope['user'].username

        }))

    @database_sync_to_async
    def save_comments(self, msg):
        user = self.scope['user']
        file = get_object_or_404(FileContainer, pk=self.context['pk'])
        perm = file.has_perm_comment(user)
        print(perm)
        if perm :
            file.comments.create(owner=user, text=msg)
        
