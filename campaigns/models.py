from django.db import models

class Game(models.Model):
    """Модель игры (из онтологии)"""
    name = models.CharField(max_length=200)
    platform = models.CharField(max_length=50, choices=[
        ('ios', 'iOS'),
        ('android', 'Android'),
        ('web', 'Web')
    ])
    version = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.name} ({self.platform})"

class Campaign(models.Model):
    """Модель рекламной кампании (из онтологии)"""
    name = models.CharField(max_length=200)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Banner(models.Model):
    """Модель баннера (из онтологии)"""
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='banners')
    title = models.CharField(max_length=100)
    image_url = models.URLField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} - {self.campaign.name}"
