from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include(('registration.urls'))),
    path('canchas/', include('canchas.urls')),
    path('clubes/', include('clubes.urls')),
]
