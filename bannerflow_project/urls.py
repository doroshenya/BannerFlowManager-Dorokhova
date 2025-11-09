from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bannerflow_app.urls')),  # УБРАТЬ точку!
]