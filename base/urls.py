from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('room/', views.room, name='home'),
    path('main/', views.main, name='main'),
]
