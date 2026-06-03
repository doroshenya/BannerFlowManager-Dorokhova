"""
Формы для BannerFlow Manager
"""
from django import forms
from .models import GameData, BannerTemplate, GeneratedBanner

class GameDataForm(forms.Form):
    """Простая форма для загрузки данных игры"""
    game_name = forms.CharField(
        max_length=100, 
        label='Название игры',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    player_name = forms.CharField(
        max_length=100, 
        label='Имя игрока',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    score = forms.IntegerField(
        label='Счет',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    level = forms.IntegerField(
        label='Уровень',
        min_value=1,
        max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    data_file = forms.FileField(
        label='Файл данных (JSON или CSV)',
        help_text='Загрузите файл с данными игры в формате JSON или CSV',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    
    def clean_data_file(self):
        """Валидация файла"""
        data_file = self.cleaned_data.get('data_file')
        if data_file:
            import os
            ext = os.path.splitext(data_file.name)[1].lower()
            if ext not in ['.json', '.csv']:
                raise forms.ValidationError('Файл должен быть в формате JSON или CSV')
        return data_file

class GenerateBannerForm(forms.Form):
    """Форма для генерации баннера"""
    name = forms.CharField(
        max_length=100,
        label='Название баннера',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    template = forms.ModelChoiceField(
        queryset=BannerTemplate.objects.all(),
        label='Шаблон',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    game_data = forms.ModelChoiceField(
        queryset=GameData.objects.all(),
        label='Данные игры',
        widget=forms.Select(attrs={'class': 'form-control'})
    )