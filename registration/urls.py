# accounts/urls.py
from django.urls import path
from .views import SignUpView, CustomLoginView, ProfileUpdateView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
]