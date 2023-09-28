from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, Profile
from .forms import RoomForm, TopicCreationFrom, UserUpdateForm, ProfileUpdateForm, UserRegisterForm

# Create your views here.


def loginPage(request):
    page = 'login'
    if (request.user.is_authenticated):
        return redirect('home')

    if (request.method == 'POST'):
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "username or password does not exist")

    context = {'page': page}
    return render(request, 'app1/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    page = 'register'
    form = UserCreationForm()
    # profile_form = ProfileUpdateForm(request.POST,
    #                                  request.FILES,
    #                                  instance=request.user.profile)

    if (request.method == "POST"):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        # if form.is_valid() and profile_form.is_valid():
        #     user = form.save(commit=False)
        #     user.username = user.username.lower()
        #     user.save()
        #     profile_form.save()
        #     login(request, user)
        #     return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    # context = {'page': page, 'form': form, 'profile_form': profile_form}
    context = {'page': page, 'form': form}
    return render(request, 'app1/login_register.html', context)


def home(request):
    q = request.GET.get('q')if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(
        name__icontains=q) | Q(description__icontains=q))
    # rooms = Room.objects.all()

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__name__icontains=q))
    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'app1/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if (request.method == "POST"):
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )

        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'app1/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    user_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': user_messages, 'topics': topics}
    return render(request, 'app1/profile.html', context)


def topicsPage(request):
    q = request.GET.get('q')if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(Q(name__icontains=q))
    context = {'topics': topics}
    return render(request, 'app1/topics.html', context)


def activityPage(request):
    room_messages = Message.objects.all()
    context = {'room_messages': room_messages}
    return render(request, 'app1/activity.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('room_name'),
            description=request.POST.get('room_about'),
        )
        return redirect('home')
        # form = RoomForm(request.POST)
        # if (form.is_valid()):
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        #     return redirect('home')
    context = {'form': form}
    return render(request, 'app1/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse("You don't have the permission to be here.")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('room_name')
        room.topic = topic
        room.description = request.POST.get('room_about')
        room.save()
        return redirect('home')
        # form = RoomForm(request.POST, instance=room)
        # if (form.is_valid()):
        #     form.save()
        #     return redirect('home')

    context = {'form': form, 'room': room, 'topics': topics}
    return render(request, 'app1/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You don't have the permission to be here.")

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'app1/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("You don't have the permission to be here.")

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'app1/delete.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):
    form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=request.user.profile)

    if (request.method == "POST"):
        form = UserUpdateForm(request.POST, request.FILES,
                              instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, instance=request.user.profile)

        if (form.is_valid() and profile_form.is_valid()):
            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            form.save()
            profile_form.save()
            return redirect('home')

    context = {'form': form, 'profile_form': profile_form}

    # context = {'form': form}
    return render(request, 'app1/update-user.html', context)


@login_required(login_url='login')
def createTopic(request):
    form = TopicCreationFrom()
    if (request.method == "POST"):
        form = TopicCreationFrom(request.POST)
        if (form.is_valid()):
            form.save()
            return redirect('home')
        else:
            messages.error("The topic already exists")
    context = {'form': form}
    return render(request, 'app1/create-topic.html', context)
