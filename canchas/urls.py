from django.contrib import admin
from django.urls import path, include
from canchas.views import FieldListView, FieldUpdateView, FieldCreateView
from canchas import views

urlpatterns = [
    path('list/', FieldListView.as_view() , name='canchas_list'),
    path('update/<int:pk>/', FieldUpdateView.as_view(), name='cancha_update'),
    path('createField/',  FieldCreateView.as_view(), name='create_field'),
    path('clients_reservations/',  views.clients_reservations, name='clients_reservations'),
    path('client_resevation_delete/<int:reservation_id>/',  views.delete_client_reservation, name='client_reservation_delete'),
]
