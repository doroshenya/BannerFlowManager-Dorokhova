from django.http import HttpResponse, JsonResponse
from .models import Banner

def home(request):
    return HttpResponse("БаннерФлоу Менеджер работает!")

def api_banners(request):
    """API для получения баннеров"""
    banners = Banner.objects.all()
    
    banner_list = []
    for banner in banners:
        banner_list.append({
            'id': banner.id,
            'title': banner.title,
            'image_url': banner.image_url
        })
    
    return JsonResponse({'banners': banner_list})