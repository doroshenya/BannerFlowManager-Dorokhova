from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
import os

def validate_media_file(value):
    """Валидатор для медиафайлов - только PNG, JPG, MP4"""
    valid_extensions = ['.png', '.jpg', '.jpeg', '.mp4']
    
    # Проверка расширения
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(
            f'Неподдерживаемый формат файла. Разрешенные форматы: PNG, JPG, MP4'
        )

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('marketer', 'Маркетолог'),
        ('analyst', 'Аналитик'),
        ('admin', 'Администратор'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='marketer')
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

class Campaign(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('active', 'Активна'),
        ('paused', 'Приостановлена'),
        ('stopped', 'Остановлена'),
    ]
    
    PLATFORM_CHOICES = [
        ('iOS', 'iOS'),
        ('Android', 'Android'),
        ('Both', 'iOS и Android'),
    ]
    
    name = models.CharField(max_length=255, verbose_name="Название кампании")
    budget = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        verbose_name="Бюджет"
    )
    start_date = models.DateTimeField(default=timezone.now, verbose_name="Дата начала")
    end_date = models.DateTimeField(default=timezone.now, verbose_name="Дата окончания")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Статус")
    target_geolocation = models.JSONField(
        default=list, 
        verbose_name="Геолокация",
        help_text="Список стран/регионов для таргетинга"
    )
    target_platform = models.CharField(
        max_length=10, 
        choices=PLATFORM_CHOICES,
        default='Both',
        verbose_name="Целевая платформа"
    )
    target_game_version = models.CharField(
        max_length=50, 
        blank=True, 
        verbose_name="Версия игры"
    )
    is_ab_test = models.BooleanField(default=False, verbose_name="A/B тест")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Создатель")
    created_at = models.DateTimeField(auto_now_add=True)

    def activate(self):
        """Активировать кампанию"""
        self.status = 'active'
        self.save()
        return f"Кампания '{self.name}' активирована"

    def pause(self):
        """Приостановить кампанию"""
        self.status = 'paused'
        self.save()
        return f"Кампания '{self.name}' приостановлена"

    def stop(self):
        """Остановить кампанию"""
        self.status = 'stopped'
        self.save()
        return f"Кампания '{self.name}' остановлена"

    @property
    def status_color(self):
        colors = {
            'draft': 'secondary',
            'active': 'success', 
            'paused': 'warning',
            'stopped': 'danger'
        }
        return colors.get(self.status, 'secondary')

    def __str__(self):
        return self.name

class Banner(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Изображение'),
        ('video', 'Видео'),
    ]
    
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, verbose_name="Кампания")
    title = models.CharField(max_length=255, verbose_name="Название баннера")
    media_file = models.FileField(
    upload_to='banners/%Y/%m/%d/', 
    verbose_name="Медиафайл",
    help_text="Поддерживаемые форматы: PNG, JPG, MP4",
    validators=[validate_media_file]
)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, verbose_name="Тип медиа")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def save(self, *args, **kwargs):
        # Автоматическое определение типа медиа
        if self.media_file:
            extension = self.media_file.name.split('.')[-1].lower()
            if extension in ['png', 'jpg', 'jpeg', 'gif']:
                self.media_type = 'image'
            elif extension in ['mp4', 'avi', 'mov']:
                self.media_type = 'video'
        super().save(*args, **kwargs)

    def clean(self):
        """Дополнительная валидация при сохранении"""
        super().clean()
        if self.media_file:
            validate_media_file(self.media_file)

    def __str__(self):
        return self.title

class ABTest(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название теста")
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, verbose_name="Кампания")
    banners = models.ManyToManyField(Banner, verbose_name="Баннеры для теста")
    audience_segment = models.CharField(max_length=100, verbose_name="Сегмент аудитории")
    start_date = models.DateTimeField(default=timezone.now, verbose_name="Дата начала")
    end_date = models.DateTimeField(default=timezone.now, verbose_name="Дата окончания")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CampaignStatistics(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, verbose_name="Кампания")
    date = models.DateField(default=timezone.now, verbose_name="Дата")
    impressions = models.IntegerField(default=0, verbose_name="Показы")
    clicks = models.IntegerField(default=0, verbose_name="Клики")
    conversions = models.IntegerField(default=0, verbose_name="Конверсии")
    
    class Meta:
        verbose_name = "Статистика кампании"
        verbose_name_plural = "Статистика кампаний"
    
    @property
    def ctr(self):
        """CTR (Click-Through Rate) в процентах"""
        return round((self.clicks / self.impressions * 100), 2) if self.impressions > 0 else 0

    def __str__(self):
        return f"Статистика {self.campaign.name} за {self.date}"
    
class BannerTemplate(models.Model):
    """Шаблон для генерации интерактивных HTML5 баннеров"""
    TEMPLATE_TYPES = [
        ('score', 'Баннер со счетом'),
        ('achievement', 'Баннер с достижением'),
        ('level', 'Баннер с уровнем'),
        ('custom', 'Пользовательский шаблон'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Название шаблона")
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPES, default='custom', verbose_name="Тип шаблона")
    html_template = models.TextField(verbose_name="HTML шаблон", help_text="Используйте {{ переменные }} для подстановки")
    css_styles = models.TextField(verbose_name="CSS стили")
    javascript = models.TextField(verbose_name="JavaScript код", blank=True, help_text="Для интерактивности")
    width = models.IntegerField(default=300, verbose_name="Ширина (px)")
    height = models.IntegerField(default=250, verbose_name="Высота (px)")
    preview_image = models.ImageField(upload_to='templates/previews/', blank=True, verbose_name="Превью")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Шаблон баннера"
        verbose_name_plural = "Шаблоны баннеров"
    
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"

class GameData(models.Model):
    """Данные из игры для генерации баннеров"""
    GAME_TYPES = [
        ('platformer', 'Платформер'),
        ('rpg', 'RPG'),
        ('shooter', 'Шутер'),
        ('strategy', 'Стратегия'),
        ('custom', 'Другая'),
    ]
    
    game_name = models.CharField(max_length=100, verbose_name="Название игры")
    game_type = models.CharField(max_length=20, choices=GAME_TYPES, default='custom', verbose_name="Тип игры")
    player_name = models.CharField(max_length=100, verbose_name="Имя игрока")
    score = models.IntegerField(default=0, verbose_name="Счет")
    level = models.IntegerField(default=1, verbose_name="Уровень")
    play_time = models.IntegerField(default=0, verbose_name="Время игры (минуты)")
    achievements = models.JSONField(default=list, verbose_name="Достижения")
    data_file = models.FileField(upload_to='game_data/', verbose_name="Файл данных игры", help_text="JSON или CSV файл")
    imported_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Данные игры"
        verbose_name_plural = "Данные игр"
    
    def __str__(self):
        return f"{self.game_name}: {self.player_name} (Ур. {self.level})"

class GeneratedBanner(models.Model):
    """Сгенерированный интерактивный баннер"""
    name = models.CharField(max_length=100, verbose_name="Название баннера")
    template = models.ForeignKey(BannerTemplate, on_delete=models.CASCADE, verbose_name="Шаблон")
    game_data = models.ForeignKey(GameData, on_delete=models.CASCADE, verbose_name="Данные игры")
    html_content = models.TextField(verbose_name="HTML содержимое")
    godot_export = models.FileField(upload_to='exports/godot/', blank=True, verbose_name="Экспорт для Godot")
    preview_url = models.URLField(blank=True, verbose_name="URL предпросмотра")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Сгенерированный баннер"
        verbose_name_plural = "Сгенерированные баннеры"
    
    def __str__(self):
        return self.name