from django.core.mail import send_mail
from .models import Campaign, Banner

class BannerService:
    @staticmethod
    def get_active_banners(platform=None):
        """Получить активные баннеры с фильтром по платформе"""
        campaigns = Campaign.objects.filter(is_active=True)
        
        if platform and platform in ['iOS', 'Android']:
            campaigns = campaigns.filter(target_platform__in=[platform, 'Both'])
        
        banners = Banner.objects.filter(campaign__in=campaigns)
        return banners
    
    @staticmethod
    def check_budget_and_notify(campaign):
        """Проверить бюджет кампании и отправить уведомление"""
        # Заглушка для тестов
        return False
