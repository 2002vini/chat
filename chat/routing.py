from django.urls import path
from . import consumers
from . import views
websocket_urlpatterns = [
    path('ws/direct/<str:room_id>/', consumers.ChatConsumer.as_asgi()),       # .as_asgi is done cause our ChatConsumer is an asynchronous function
    path('ws/status/', consumers.OnlineConsumer.as_asgi()),
    path('ws/notify/',consumers.NotificationConsumer.as_asgi()),
    path('ws/group/<str:group_id>/',consumers.GroupConsumer.as_asgi()),
    
]


