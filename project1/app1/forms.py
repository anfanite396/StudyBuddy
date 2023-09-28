from django.forms import ModelForm
from .models import Room, Profile, Topic
from django.contrib.auth.models import User


class UserRegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password']


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email']


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['user_bio', 'birth_date', 'avatar']


class TopicCreationFrom(ModelForm):
    class Meta:
        model = Topic
        fields = ['name']
