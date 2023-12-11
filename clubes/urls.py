from django.contrib import admin
from django.urls import path, include
from clubes import views
from .views import ClubUpdateView

urlpatterns = [
    path('all/', views.fetchClubs, name='all'),
    path('settings/', ClubUpdateView.as_view(), name='club_settings')
]
