import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import Campaign, Banner

# Базовые тесты моделей
class TestCampaignModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com',
            password='testpass123'
        )
    
    def test_campaign_creation(self):
        """Позитивный тест: создание кампании"""
        campaign = Campaign.objects.create(
            name="Test Campaign",
            budget=1000.00,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=7),
            target_platform='Both',
            is_active=True,
            created_by=self.user
        )
        self.assertEqual(campaign.name, "Test Campaign")
        self.assertEqual(campaign.budget, 1000.00)

    def test_campaign_string_representation(self):
        """Тест строкового представления"""
        campaign = Campaign.objects.create(
            name="Summer Campaign",
            budget=500.00,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=7),
            target_platform='iOS',
            created_by=self.user
        )
        self.assertEqual(str(campaign), "Summer Campaign")

class TestBannerModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='bannertest', 
            password='testpass123'
        )
        self.campaign = Campaign.objects.create(
            name="Banner Test Campaign",
            budget=1000.00,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=7),
            target_platform='Both',
            created_by=self.user
        )
    
    def test_banner_creation(self):
        """Тест создания баннера"""
        banner = Banner.objects.create(
            campaign=self.campaign,
            name="Test Banner",
            format_type="PNG",
            url="http://example.com/banner.png"
        )
        self.assertEqual(banner.name, "Test Banner")
        self.assertEqual(banner.format_type, "PNG")

# Параметризованные тесты
@pytest.mark.parametrize("format_type,expected_valid", [
    ('PNG', True),
    ('JPG', True),
    ('MP4', True),
])
def test_banner_format_types(format_type, expected_valid):
    """Параметризованный тест форматов баннеров"""
    user = User.objects.create_user(username='formattest', password='testpass123')
    campaign = Campaign.objects.create(
        name="Format Test Campaign",
        budget=1000.00,
        start_date=timezone.now(),
        end_date=timezone.now() + timedelta(days=7),
        target_platform='Both',
        created_by=user
    )
    
    banner = Banner.objects.create(
        campaign=campaign,
        name=f"Test {format_type}",
        format_type=format_type,
        url=f"http://example.com/banner.{format_type.lower()}"
    )
    assert banner.format_type == format_type

# Тесты представлений
class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='viewtest',
            password='testpass123'
        )
        self.campaign = Campaign.objects.create(
            name="View Test Campaign",
            budget=1000.00,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=7),
            target_platform='Both',
            is_active=True,
            created_by=self.user
        )
        self.banner = Banner.objects.create(
            campaign=self.campaign,
            name="View Test Banner",
            format_type="PNG",
            url="http://example.com/view_banner.png"
        )
        
    def test_home_view(self):
        """Тест главной страницы"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_api_banners_view(self):
        """Тест API баннеров"""
        response = self.client.get('/api/banners/')
        self.assertEqual(response.status_code, 200)
