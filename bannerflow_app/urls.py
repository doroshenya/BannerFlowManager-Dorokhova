from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/banners/', views.api_banners, name='api_banners'),
]
