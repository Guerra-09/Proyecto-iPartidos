from django.contrib import admin
from django.urls import path, include
from canchas import views

urlpatterns = [
    path('see/', views.canchaScreen, name='canchas')
]
