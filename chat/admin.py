from django.contrib import admin
from .models import *


class CustomChatRoom(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'room_id']

class CustomChatMessage(admin.ModelAdmin):
    list_display = ['id', 'sender', 'room', 'created_at', 'message_content']

class CustomProfile(admin.ModelAdmin):
    list_display = ['user', 'unique_id','last_seen','last_text']
    ordering=['-last_seen']

class CustomChatNotification(admin.ModelAdmin):
    list_display=['chat','chat_sent_to','is_seen']

class CustomSocialGroup(admin.ModelAdmin):
    list_display = ['name', 'admin', 'participants']

class CustomGroupMessage(admin.ModelAdmin):
    list_display = ['group', 'sender']

class CustomFriendRequest(admin.ModelAdmin):
    list_display=['from_user','to_user','accept']

admin.site.register(Profile, CustomProfile)
admin.site.register(ChatRoom, CustomChatRoom)
admin.site.register(ChatMessage, CustomChatMessage)
admin.site.register(ChatNotification,CustomChatNotification)
admin.site.register(SocialGroup,CustomSocialGroup)
admin.site.register(GroupMessage,CustomGroupMessage)
admin.site.register(FriendRequest,CustomFriendRequest)


