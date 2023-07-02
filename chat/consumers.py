from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import *


# Get Group ID
# add current channel to specified group
# inform websocket client that connection has been accepted. Its necessary to complete handshake
class GroupConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']

        await self.channel_layer.group_add(
            self.group_id,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_sender = data['message_sender']
        message_content = data['message_content']

        await self.channel_layer.group_send(        # this line sends message to all the channels in the group
            self.group_id,
            {
                'type': "handleGroupChat",      # this method will be used to send message individually to all users
                'message_content': message_content,
                'message_sender': message_sender
            }
        )
        await self.save_message(message_sender, message_content, self.group_id)

    async def handleGroupChat(self, event):
        message_content = event['message_content']
        message_sender = event['message_sender']

        await self.send(text_data=json.dumps({
            'message_content': message_content,
            'message_sender': message_sender
        }))

    @sync_to_async
    def save_message(self, sender, message, group_id):
        user = User.objects.get(username=sender)
        sender_profile = Profile.objects.get(user=user)
        group = SocialGroup.objects.get(group_id=group_id)
        group_obj = GroupMessage(group=group, sender=sender_profile, message_content=message)
        group_obj.save()
        sender_profile.save()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']

        await self.channel_layer.group_add(
            self.room_id,
            self.channel_name       # channel_name will be automatically be created for each user
        )
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data['message_content']
        message_sender = data['message_sender']
        
        

        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': 'handleChatEvent',      # name of the function that handles chat event-
                'message_content': message_content,
                'message_sender': message_sender
            }
        )
        await self.save_message(message_sender, self.room_id, message_content)

    async def handleChatEvent(self, event):
        message_content = event['message_content']
        message_sender = event['message_sender']

        await self.send(text_data = json.dumps({
            'message_content': message_content,
            'message_sender': message_sender,
        }))

    @sync_to_async
    def save_message(self, message_sender, room_id, message_content):
        sender = User.objects.get(username=message_sender)
        sender_profile=Profile.objects.get(user=sender)
        sender_profile.last_text=message_content
        room = ChatRoom.objects.get(room_id=room_id)
        chat_obj = ChatMessage(sender=sender, room=room, message_content=message_content)
        chat_obj.save()
        sender_profile.save()
        # ChatNotification.objects.create(chat=chat_obj,chat_sent_to=user)
        # print("chat notification has been created")


class OnlineConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "online_users_pool"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None):
        data = json.loads(text_data)
        status = data['status']
        logged_in_user = self.scope["user"]
        await self.setUserStatus(logged_in_user, status)
        

    @sync_to_async
    def setUserStatus(self, username, status):
        user = User.objects.get(username=username)
        profile_user = Profile.objects.get(user=user)
        if status == 'online':
            profile_user.online_status = True
            profile_user.save()
        else:
            profile_user.online_status = False
            profile_user.save()


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        my_id=self.scope['user'].id
        self.room_group_name=f'{my_id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def send_notification(self, event):
        print("send notification")
        data = json.loads(event.get('value'))
        count = data['count']
        print(event)
        await self.send(text_data=json.dumps({
            'count':count
        }))

    async def disconnect(self, code):
        print("disconnected")
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )