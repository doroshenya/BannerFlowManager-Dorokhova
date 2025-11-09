from django.db import models

class Campaign(models.Model):
    """Модель рекламной кампании (из ваших требований)"""
    name = models.CharField(max_length=200, verbose_name="Название кампании")
    budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Бюджет")
    start_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата начала")
    is_active = models.BooleanField(default=False, verbose_name="Активна")
    
    class Meta:
        verbose_name = "Рекламная кампания"
        verbose_name_plural = "Рекламные кампании"
    
    def activate(self):
        """Активировать кампанию (требование №5)"""
        self.is_active = True
        self.save()
        return f"Кампания '{self.name}' активирована"
    
    def deactivate(self):
        """Деактивировать кампанию (требование №5)"""
        self.is_active = False
        self.save()
        return f"Кампания '{self.name}' деактивирована"
    
    def __str__(self):
        return f"{self.name} (Бюджет: {self.budget}, Активна: {self.is_active})"

class Banner(models.Model):
    """Модель баннера (из вашей онтологии)"""
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, verbose_name="Кампания")
    image_url = models.URLField(verbose_name="URL изображения")
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    
    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"
    
    def __str__(self):
        return f"Баннер: {self.title}"