from django.urls import path
from . import views

urlpatterns = [
    path('', views.temp, name='temp'),
    path('add/', views.add, name='add'),
    path('add/sum/', views.sum, name='sum'),
]
