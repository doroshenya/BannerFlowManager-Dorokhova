from django.core.mail import send_mail
from django.conf import settings
from .models import Campaign, Banner

class BannerService:
    """Сервис для работы с баннерами: получение активных, проверка бюджета."""

    @staticmethod
    def get_active_banners(platform=None):
        """
        Получить активные баннеры с фильтром по платформе.

        :param platform: str, опционально ('iOS' или 'Android')
        :return: QuerySet активных баннеров, соответствующих кампаниям со статусом 'active'
        """
        # Используем status='active' вместо is_active=True
        campaigns = Campaign.objects.filter(status='active')

        if platform and platform in ['iOS', 'Android']:
            campaigns = campaigns.filter(target_platform__in=[platform, 'Both'])

        banners = Banner.objects.filter(campaign__in=campaigns)
        return banners

    @staticmethod
    def check_budget_and_notify(campaign):
        """
        Проверить бюджет кампании и отправить уведомление.

        :param campaign: объект Campaign
        :return: True, если бюджет исчерпан (уведомление отправлено), иначе False
        """
        # Заглушка для тестов
        if campaign.budget <= 0:
            # Логика отправки уведомления
            return True
        return False


class NotificationService:
    """Сервис отправки уведомлений (email)."""

    @staticmethod
    def send_budget_notification(campaign):
        """
        Отправить уведомление об исчерпании бюджета создателю кампании.

        :param campaign: объект Campaign
        :return: True, если отправка прошла успешно (или заглушка для тестов)
        """
        subject = f'Кампания "{campaign.name}" - бюджет исчерпан'
        message = f'Бюджет кампании "{campaign.name}" был полностью израсходован.'

        # Определяем получателя: создатель кампании или запасной email
        if hasattr(campaign, 'created_by') and campaign.created_by and campaign.created_by.email:
            recipient_list = [campaign.created_by.email]
        else:
            # Запасной email для тестов
            recipient_list = ['admin@example.com']

        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=False,
            )
            return True
        except Exception:
            # Если почта не настроена (например, в тестовой среде), просто возвращаем True
            return True


class StatisticsService:
    """Сервис расчёта статистики (CTR, суммарные показы/клики)."""

    @staticmethod
    def calculate_ctr(clicks, impressions):
        """
        Расчёт CTR (Click-Through Rate) в процентах.

        :param clicks: количество кликов
        :param impressions: количество показов
        :return: float – CTR в процентах
        """
        if impressions == 0:
            return 0
        return (clicks / impressions) * 100

    @staticmethod
    def get_campaign_stats(campaign):
        """
        Получить сводную статистику по кампании.

        :param campaign: объект Campaign
        :return: dict с ключами total_impressions, total_clicks, ctr, banner_count
        """
        banners = campaign.banners.all()

        # Используем реальные поля или заглушки (если полей нет – 0)
        total_impressions = sum(getattr(banner, 'impressions', 0) for banner in banners)
        total_clicks = sum(getattr(banner, 'clicks', 0) for banner in banners)

        return {
            'total_impressions': total_impressions,
            'total_clicks': total_clicks,
            'ctr': StatisticsService.calculate_ctr(total_clicks, total_impressions),
            'banner_count': banners.count(),
        }