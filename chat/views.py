from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse

from chat.models import Room, Message


@login_required(login_url='login')
def index(request):
    users = User.objects.all().exclude(username=request.user)
    return render(request, "chat/index.html", {"users": users})




@login_required(login_url='login')
def room(request, room_name):
    room = Room.objects.get(id=room_name)
    users = User.objects.all().exclude(username=request.user)
    messages = Message.objects.filter(room=room)
    context = {
        "room": room,
        "users": users,
        "room_name": room_name,
        "messages": messages
    }
    return render(request, "chat/room_v2.html", context)




@login_required(login_url='login')
def start_chat(request, username):
    second_user = User.objects.get(username=username)
    try:
        room = Room.objects.get(first_user=request.user, second_user=second_user)
    except Room.DoesNotExist:
        try:
            room = Room.objects.get(second_user=request.user, first_user=second_user)
        except Room.DoesNotExist:
            room = Room.objects.create(first_user=request.user, second_user=second_user)
    return redirect("room", room.id)




def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
    return render(request, "chat/login.html")
