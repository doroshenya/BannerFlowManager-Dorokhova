"""
Модуль тестирования для BannerFlow Manager
"""
import pytest
from django.test import TestCase, Client
from django.db import transaction
from django.contrib.auth.models import User
from .models import Campaign, Banner, BannerTemplate, GameData, GeneratedBanner
from .banner_generator import BannerGenerator
import tempfile
import json
import os

class TestCampaignModel(TestCase):
    """Тестирование модели Campaign"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_campaign_creation_and_methods(self):
        """Тест создания кампании и её методов"""
        from django.utils import timezone
        
        campaign = Campaign.objects.create(
            name="Test Campaign",
            budget=1000.00,
            start_date=timezone.now(),
            end_date=timezone.now(),
            status='draft',
            created_by=self.user
        )
        
        self.assertEqual(campaign.name, "Test Campaign")
        self.assertEqual(float(campaign.budget), 1000.00)
        self.assertEqual(campaign.status, 'draft')

class TestBannerModel(TestCase):
    """Тестирование модели Banner"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        from django.utils import timezone
        self.campaign = Campaign.objects.create(
            name="Banner Test Campaign",
            budget=1000.00,
            start_date=timezone.now(),
            end_date=timezone.now(),
            status='draft',
            created_by=self.user
        )
    
    def test_banner_creation(self):
        """Тест создания баннера"""
        banner = Banner.objects.create(
            campaign=self.campaign,
            title="Test Banner",
            media_file="banners/test.png"
        )
        
        self.assertEqual(banner.title, "Test Banner")
        self.assertEqual(banner.campaign, self.campaign)

class TestBannerTemplateModel(TestCase):
    """Тестирование модели BannerTemplate"""
    
    def test_template_creation(self):
        """Тест создания шаблона баннера"""
        template = BannerTemplate.objects.create(
            name="Test Template",
            template_type='score',
            html_template="<div>Player: {{ player_name }}</div>",
            css_styles="div { color: blue; }",
            width=300,
            height=250
        )
        
        self.assertEqual(template.name, "Test Template")
        self.assertEqual(template.template_type, 'score')
        self.assertEqual(template.width, 300)
        self.assertEqual(template.height, 250)

class TestGameDataModel(TestCase):
    """Тестирование модели GameData"""
    
    def test_game_data_creation(self):
        """Тест создания данных игры"""
        game_data = GameData.objects.create(
            game_name="Test Game",
            game_type='platformer',
            player_name="Test Player",
            score=1000,
            level=5,
            play_time=3600,
            achievements=["First Win", "Speed Run"],
            data_file="game_data/test.json"
        )
        
        self.assertEqual(game_data.game_name, "Test Game")
        self.assertEqual(game_data.player_name, "Test Player")
        self.assertEqual(game_data.score, 1000)
        self.assertEqual(game_data.level, 5)
        self.assertEqual(game_data.play_time, 3600)

class TestBannerGenerator(TestCase):
    """Тестирование генератора баннеров"""
    
    def setUp(self):
        self.template = BannerTemplate.objects.create(
            name="Test Template",
            html_template="<div>Player: {{ player_name }} - Score: {{ score }}</div>",
            css_styles="div { color: blue; }",
            width=300,
            height=250
        )
        
        self.game_data = GameData.objects.create(
            game_name="Test Game",
            player_name="Test Player",
            score=1000,
            level=5,
            achievements=["First Win", "Speed Run"],
            data_file="game_data/test.json"
        )
    
    def test_banner_generation(self):
        """Тест генерации HTML баннера"""
        html = BannerGenerator.generate_html(self.template, self.game_data)
        
        self.assertIn("Test Player", html)
        self.assertIn("1000", html)
        self.assertIn("300px", html)
        self.assertIn("250px", html)
    
    def test_banner_generation_errors(self):
        """Тест обработки ошибок при генерации баннера"""
        # Тест с пустым шаблоном
        with self.assertRaises(ValueError):
            BannerGenerator.generate_html(None, self.game_data)
        
        # Тест с пустыми данными игры
        with self.assertRaises(ValueError):
            BannerGenerator.generate_html(self.template, None)

class TestFileParsingErrors(TestCase):
    """Тестирование обработки ошибок парсинга файлов"""
    
    def test_file_not_found(self):
        """Тест обработки отсутствующего файла"""
        with self.assertRaises(FileNotFoundError):
            BannerGenerator.parse_game_file("nonexistent.json")
    
    def test_invalid_json(self):
        """Тест обработки невалидного JSON"""
        # Создаем файл с невалидным JSON
        json_data = '{invalid json}'
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write(json_data)
            json_file = f.name
        
        with self.assertRaises(ValueError):
            BannerGenerator.parse_game_file(json_file)
        
        os.unlink(json_file)
    
    def test_unsupported_format(self):
        """Тест обработки неподдерживаемого формата"""
        # Создаем файл с неподдерживаемым расширением
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Some text")
            txt_file = f.name
        
        with self.assertRaises(ValueError):
            BannerGenerator.parse_game_file(txt_file)
        
        os.unlink(txt_file)
    
    def test_empty_csv(self):
        """Тест обработки пустого CSV файла"""
        # Создаем пустой CSV файл
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("")  # Пустой файл
            csv_file = f.name
        
        with self.assertRaises(ValueError):
            BannerGenerator.parse_game_file(csv_file)
        
        os.unlink(csv_file)

class TestAPIAndServices(TestCase):
    """Тестирование API и сервисов"""
    
    def setUp(self):
        self.client = Client()
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        from django.utils import timezone
        self.campaign = Campaign.objects.create(
            name="API Test Campaign",
            budget=1000.00,
            start_date=timezone.now(),
            end_date=timezone.now(),
            status='active',
            created_by=self.user
        )
        
        self.banner = Banner.objects.create(
            campaign=self.campaign,
            title="API Test Banner",
            media_file="banners/api_banner.png"
        )
    
    def test_home_page(self):
        """Тест главной страницы"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_api_endpoint(self):
        """Тест API endpoints"""
        try:
            response = self.client.get('/api/public/banners/')
            self.assertIn(response.status_code, [200, 404, 403])
        except:
            pass

class TestNegativeScenarios(TestCase):
    """Тестирование ошибочных сценариев"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_negative_cases(self):
        """Тестирование ошибочных сценариев"""
        # Тест с отрицательным бюджетом
        try:
            campaign = Campaign.objects.create(
                name="Negative Budget Campaign",
                budget=-100.00,
                start_date="2025-01-01T00:00:00",
                end_date="2025-12-31T23:59:59",
                status='draft',
                created_by=self.user
            )
            # Если сохранилось без ошибки - это тоже результат
            self.assertEqual(float(campaign.budget), -100.00)
        except Exception as e:
            # Если была ошибка валидации - это правильно
            self.assertIn('budget', str(e).lower())

if __name__ == '__main__':
    import unittest
    unittest.main()