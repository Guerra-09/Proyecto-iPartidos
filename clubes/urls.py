from django.contrib import admin
from django.urls import path, include
from clubes import views

urlpatterns = [
    path('see/', views.home, name='clubes')
]
