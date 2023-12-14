from django.urls import path
from reservation import views

urlpatterns = [
    path('dateSelection/<int:field_id>', views.index, name='reservation'),
    path('payment/', views.payment, name='payment'),
    path('payment_success/', views.payment_success, name='payment_success')
]
