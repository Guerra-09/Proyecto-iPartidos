from django.contrib import admin
from django.urls import path, include
from canchas.views import FieldListView, FieldUpdateView, FieldCreateView

urlpatterns = [
    path('list/', FieldListView.as_view() , name='canchas_list'),
    path('update/<int:pk>/', FieldUpdateView.as_view(), name='cancha_update'),
    path('createField/',  FieldCreateView.as_view(), name='create_field'),
]
