from django.urls import path
from . import views

urlpatterns = [
    # Основные страницы
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Генератор баннеров (основная функциональность проекта)
    path('generator/', views.banner_generator, name='banner_generator'),
    path('generate/', views.generate_banner, name='generate_banner'),
    path('banner/preview/<int:banner_id>/', views.banner_preview, name='banner_preview'),
    path('banner/export/<int:banner_id>/', views.export_banner, name='export_banner'),
    path('banner/list/', views.banner_list, name='banner_list'),
    
    # API
    path('api/public/banners/', views.api_banners, name='public_banners'),
    
    path('upload-data/', views.upload_game_data, name='upload_game_data'),
]
