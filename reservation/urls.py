from django.urls import path
from reservation import views

urlpatterns = [
    path('index/<int:field_id>/', views.index, name='index'),
    path('dateSelection/<int:field_id>', views.index, name='reservation'),
    path('payment/', views.payment, name='payment'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('create_reservation/', views.create_reservation, name='create_reservation')
]
