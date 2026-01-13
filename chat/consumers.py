# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user == AnonymousUser():
            await self.close()
            return
        
        self.room_group_name = f"user_{self.user.id}"
        
        # Join user's personal room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'message':
            await self.handle_message(data)
        elif message_type == 'typing':
            await self.handle_typing(data)
        elif message_type == 'read_receipt':
            await self.handle_read_receipt(data)
    
    async def handle_message(self, data):
        # Save message to database
        message = await self.save_message(data)
        
        # Send to all conversation participants
        for participant in message.conversation.participants.all():
            if participant.id != self.user.id:
                await self.channel_layer.group_send(
                    f"user_{participant.id}",
                    {
                        'type': 'chat_message',
                        'message': await self.message_to_dict(message)
                    }
                )
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
    
    @database_sync_to_async
    def save_message(self, data):
        # Implementation to save message to database
        pass