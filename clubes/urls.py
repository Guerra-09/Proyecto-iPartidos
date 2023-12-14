from django.contrib import admin
from django.urls import path, include
from clubes import views
from .views import ClubUpdateView, ClubsListView, ClubClientDetailView

urlpatterns = [
    path('all/', ClubsListView.as_view(), name='all'),
    path('settings/', ClubUpdateView.as_view(), name='club_settings'),
    path('clubFields/<int:pk>', ClubClientDetailView.as_view(), name='field_detail')
]
