from django.urls import path
from . import views



app_name = 'chat'


urlpatterns = [
    # path('', views.ChatAPI.as_view(), name="ChatAPI"),
    # path('direct/<uuid:receiver_id>/', views.ChatAPI.as_view(), name="directMessage"),

    path('', views.index, name="index"),
    path('direct/<uuid:receiver_id>/', views.directMessage, name="directMessage"),
    path('group/', views.createGroup, name="createGroup"),
    path('group/<str:group_id>/', views.groupMessage, name="groupMessage"),
    #path('search/',views.search,name='search'),
    path('search/',views.usersearch.as_view(),name='search'),
    path('requests/',views.viewRequest,name='view_request'),
    path('accept/<uuid:friend_id>/',views.acceptRequest,name='accept_request'),
    path('ignore/<uuid:friend_id>/',views.ignoreRequest,name='ignore_request'),
    path('<str:role>/',views.display,name='display'),
    path('form',views.get_form),
    path('request/<uuid:receiver_id>/',views.createRequest,name='createRequest'),
]