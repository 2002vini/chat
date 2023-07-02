from django.shortcuts import render,HttpResponse,redirect
from .models import *
from .serializers import *
import hashlib
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
import json
import datetime
from datetime import datetime
from django.db.models import Q
from django.http import JsonResponse
from . models import ChatRoom
from rest_framework import viewsets
import re
from . forms import MyForm

def get_form(request):
    if request.method=='GET':
        return render(request,'form.html')
    else:
        username=request.POST.get('pattern')
        number_of_users=request.POST.get('number_of_users')
        password=request.POST.get('password')
        length=len(number_of_users)
        number_of_users=int(number_of_users)
        print(type(number_of_users))
        pattern = r'\d+'  # Regex pattern to match one or more digits
        match = re.findall(pattern, username)
        if len(match)==1:
            for i in range(1,number_of_users+1):
                name=username+str(i).zfill(max(3,length))
                User.objects.create(username=name,password=password)
                print(name)
        else:
            number=int(match[-1].lstrip('0'))
            for i in range(number,number+number_of_users+1):
                name=username.replace(match[-1],"")+str(i).zfill(max(3,length))
                User.objects.create(username=name,password=password)
                print(name)
                
            
        
        return HttpResponse("hello")

@login_required
def index(request):
    #setParameters(friends,user_profile)
    request_profile=Profile.objects.get(user=request.user)
    #friends=Profile.objects.filter(user__in=request_profile.friends.all())
    friends=Profile.objects.exclude(user=request.user)
    params = {
        'friends': friends,
    }
    return render(request, "index.html", params)

@login_required
def display(request,role):
    print("in display function")
    if role=='teachers':
        friends=Profile.objects.filter(is_teacher=True)
        params={
            'teachers':friends
        }
       
        return render(request,"index.html",params)
    elif role=='educators':
        friends=Profile.objects.filter(is_educator=True)
        params={
            'educators':friends
        }
        return render(request,"index.html",params)
    else:
        friends=Profile.objects.filter(is_student=True,last_text=None)
        user_profile=Profile.objects.get(user=request.user)
        friend_requests=FriendRequest.objects.filter(from_user=user_profile)
        for requests in friend_requests:
            friends=friends.exclude(unique_id=requests.to_user.unique_id)
        print("the friends to be displayed are:")
        print(friends)
    params={
        'allfriends':friends,
        'friend_requests':friend_requests,
        
    }
    return render(request,"index.html",params)


def setParameters(friends,sender):
    for friend in friends:
        roomid=getRoomHash(friend.unique_id,sender.unique_id)
        if not ChatRoom.objects.filter(room_id=roomid).exists():
            ChatRoom.objects.create(room_id=roomid)
        rooms=ChatRoom.objects.get(room_id=roomid)
        print(ChatRoom)
        messages=ChatMessage.objects.filter(room=rooms).order_by('created_at').last()
        if messages:
            friend.last_text=messages.message_content
            friend.last_seen=messages.created_at
            print(messages.created_at)
            friend.save()
            print(friend.last_seen)
        #print(friend.last_seen)
        #friend.last_seen=
        #print(friend.last_seen)

def getRoomHash(sender_id, receiver_id):
    room_name = ""
    if str(sender_id) > str(receiver_id):
        room_name = f"{sender_id}--{receiver_id}"
    else:
        room_name = f"{receiver_id}--{sender_id}"

    room_id = hashlib.sha256(room_name.encode()).hexdigest()
    return room_id


@login_required
def directMessage(request, receiver_id):
    sender = Profile.objects.get(user=request.user)
    room_id = getRoomHash(sender.unique_id, receiver_id)
    receiver=Profile.objects.get(unique_id=receiver_id)
   
    

    if not ChatRoom.objects.filter(room_id=room_id).exists():
        ChatRoom.objects.create(room_id=room_id)

    chatroom = ChatRoom.objects.get(room_id=room_id)
    messages = ChatMessage.objects.filter(room=chatroom)

    friends = Profile.objects.exclude(user=request.user)
    user_groups = SocialGroup.objects.filter(members=sender)
    receiver = Profile.objects.get(unique_id=receiver_id)
    setParameters(friends,sender)
    friend_serializer=ProfileSerializer(friends,many=True)
    print("my friends are")
    print(friends)
    params = {
        'friends': friends,
        'user_groups': user_groups,
        'room_id': chatroom.room_id,
        'messages': messages,
        'is_direct_message': True,
        'receiver': receiver,
        'friend_serializer':friend_serializer.data,
        'receiver_id':receiver_id,
    }

    return render(request, 'index.html', params)


@login_required
def createGroup(request):
    if request.method == "POST":
        admin = Profile.objects.get(user=request.user)
        group_name = request.POST['group_name']

        group_id = hashlib.sha256(group_name.encode()).hexdigest()

        if not SocialGroup.objects.filter(name=group_name).exists():
            group = SocialGroup(group_id=group_id, admin=admin, name=group_name)
            group.save()
            group.members.add(admin)
            group.save()
    return render(request, 'createGroup.html')


@login_required
def groupMessage(request, group_id):
    group = SocialGroup.objects.get(group_id=group_id)
    group_messages = GroupMessage.objects.filter(group=group)

    message = group_messages[0]

    friends = Profile.objects.exclude(user=request.user)

    sender = Profile.objects.get(user=request.user)
    user_groups = SocialGroup.objects.filter(members=sender)

    params = {
        'friends': friends,
        'user_groups': user_groups,
        'group_details': group,
        'group_messages': group_messages,
        'is_direct_message': False,
    }

    return render(request, 'index.html', params)
class createUser(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer


class usersearch(APIView):
    def get(self,request,query="",format=None):
        query=request.GET['query']
        print("in get function")
        print(query)
        stu=User.objects.filter(
        Q(username__icontains=query)|Q(last_name__icontains=query)|Q(first_name__icontains=query))
        lst=[]
        for students in stu:
            lst.append(students.username)
        print("list is")
        print(lst)
        return JsonResponse({'status':200,'data':lst})

    def post(self,request,query=None,format=None):
        print("in post method")
        query=request.POST['query']
        friends=Profile.objects.filter(Q(user__username__icontains=query)|Q(user__last_name__icontains=query)|Q(user__first_name__icontains=query))
        
        params={
            'friends':friends,
        }
        return render(request,'index.html',params)

def search(request):
    print("in search function")
    query=request.GET['query']
    print(query)
    stu=User.objects.filter(
        Q(username__icontains=query)|Q(first_name__icontains=query)|Q(last_name__icontains=query)
    )
    lst=[]
    for students in stu:
        lst.append(students.username)
    print(lst)
    return JsonResponse({'status':200,'data':lst})

def createRequest(request,receiver_id):
    to_user_profile=Profile.objects.get(unique_id=receiver_id)
    request_profile=Profile.objects.get(user=request.user)
    FriendRequest.objects.create(to_user=to_user_profile,from_user=request_profile)
    return redirect('/chat/friends/')

def viewRequest(request):
    user_profile=Profile.objects.get(user=request.user)
    requests=FriendRequest.objects.filter(to_user=user_profile)
    print("the requests received are ")
    print(requests)
    params={
        'requests':requests
    }
    return render(request,"index.html",params)

def acceptRequest(request,friend_id):
    sender_profile=Profile.objects.get(unique_id=friend_id)
    request_profile=Profile.objects.get(user=request.user)
    print(sender_profile.user.username)
    friend_request=FriendRequest.objects.get(from_user=sender_profile,to_user=request_profile)
    friend_request.accept=True
    friend_request.save()
    request_profile.friends.add(sender_profile.user)
    sender_profile.friends.add(request_profile.user)
    request_profile.save()
    sender_profile.save()
    requests=FriendRequest.objects.filter(to_user=request_profile)
    params={
       'requests':requests
    }
    return render(request,"index.html",params)

def ignoreRequest(request,friend_id):
    sender_profile=Profile.objects.get(unique_id=friend_id)
    request_profile=Profile.objects.get(user=request.user)
    friend_request=FriendRequest.objects.get(from_user=sender_profile,to_user=request_profile)
    print("before deletion")
    friend_request.delete()
    print("after deletion")
    requests=FriendRequest.objects.filter(to_user=request_profile)
    params={
        'requests':requests
    }
    return render(request,"index.html",params)
