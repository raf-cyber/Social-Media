import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from channels.db import database_sync_to_async
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['username']
        self.room_group_name = 'chat_%s' % self.room_name

        self.receiver_user = await database_sync_to_async(User.objects.get)(username=self.room_name)


        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print(f"User connected to {self.room_group_name}")

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"User disconnected from {self.room_group_name}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = data['sender']

        # Save the message to the database
        await database_sync_to_async(Message.objects.create)(
            sender=self.scope['user'],
            receiver=self.receiver_user,
            message=message
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender
            }
        )



    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        print(f"Chat message event received: {sender}: {message}")

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))
        print(f"Sending message to WebSocket: {sender}: {message}")
