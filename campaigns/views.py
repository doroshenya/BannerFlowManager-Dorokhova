from django.http import HttpResponse

def index(request):
    return HttpResponse("BannerFlow Manager - Campaigns App")
