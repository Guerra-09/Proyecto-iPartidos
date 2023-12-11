from django.contrib import admin
from django.urls import path, include
from canchas.views import FieldListView

urlpatterns = [
    path('list/', FieldListView.as_view() , name='canchas_list')
]
