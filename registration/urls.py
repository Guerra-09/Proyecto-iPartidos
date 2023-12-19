# accounts/urls.py
from django.urls import path
from . import views
from .views import SignUpView, CustomLoginView, ProfileUpdateView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('password_recovery/', views.password_recovery, name='password_recovery'),
    path('change_password/', views.change_password, name='change_password'),
    path('user_reserves/<int:pk>/', views.user_reserves, name='user_reserves'),
    path('cancel_reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('reservation_update/<int:reservation_id>/', views.change_reservation, name='reservation_update'),
    path('reservation_update_success/<int:reservation_id>/', views.confirm_reservation, name='confirm_reservation'),
]