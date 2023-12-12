from django.contrib import admin
from django.urls import path, include
from clubes import views
from .views import ClubUpdateView, FieldCreateView, ClubsListView

urlpatterns = [
    path('all/', ClubsListView.as_view(), name='all'),
    path('settings/', ClubUpdateView.as_view(), name='club_settings'),
    path('createField/',  FieldCreateView.as_view(), name='create_field'),
]
