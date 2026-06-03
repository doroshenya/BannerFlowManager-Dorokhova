import json
import csv
from django.template import Template, Context

class BannerGenerator:
    """
    Генератор интерактивных HTML5 баннеров для игр.

    Предоставляет статические методы для:
    - генерации HTML-баннера на основе шаблона и данных игры;
    - экспорта баннера в формате скрипта для Godot Engine;
    - парсинга файлов данных игры (JSON/CSV).
    """

    @staticmethod
    def generate_html(template, game_data):
        """
        Генерация HTML баннера из шаблона и данных игры.

        :param template: объект BannerTemplate с полями html_template, css_styles, javascript, width, height
        :param game_data: объект GameData с данными игрока (имя, счёт, уровень, достижения и т.д.)
        :return: str – полный HTML-код баннера (с подставленными данными)
        """
        # Подготовка контекста для шаблона
        context = {
            'player_name': game_data.player_name,
            'game_name': game_data.game_name,
            'score': game_data.score,
            'level': game_data.level,
            'play_time': game_data.play_time,
            'achievements': game_data.achievements,
            'width': template.width,
            'height': template.height,
            'template_name': template.name,
        }

        # Рендеринг HTML-шаблона (подстановка переменных вида {{ score }})
        html_template = Template(template.html_template)
        html_content = html_template.render(Context(context))

        # Формирование полного HTML-документа с обёрткой и стилями
        full_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Баннер: {game_data.game_name}</title>
    <style>
        .game-banner {{
            width: {template.width}px;
            height: {template.height}px;
            position: relative;
            overflow: hidden;
            font-family: Arial, sans-serif;
        }}
        {template.css_styles}
    </style>
</head>
<body>
    <div class="game-banner">
        {html_content}
    </div>
    
    <script>
        const gameData = {{
            player: "{game_data.player_name}",
            score: {game_data.score},
            level: {game_data.level},
            achievements: {json.dumps(game_data.achievements, ensure_ascii=False)}
        }};
        
        {template.javascript}
        
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('Баннер загружен с данными:', gameData);
            
            document.querySelector('.game-banner').addEventListener('click', function() {{
                alert(`Игрок: ${{gameData.player}}\\nСчет: ${{gameData.score}}\\nУровень: ${{gameData.level}}`);
            }});
        }});
    </script>
</body>
</html>"""

        return full_html

    @staticmethod
    def export_for_godot(html_content, banner_name, template):
        """
        Экспорт баннера для Godot Engine в виде GDScript-файла.

        :param html_content: str – HTML-код сгенерированного баннера (используется для комментария)
        :param banner_name: str – название баннера (для формирования имени файла)
        :param template: объект BannerTemplate (нужен для получения названия и размеров)
        :return: str – содержимое GDScript-файла (.gd)
        """
        # Формируем имя файла: удаляем пробелы, приводим к нижнему регистру
        safe_name = banner_name.lower().replace(' ', '_')
        godot_script = f"""# banner_{safe_name}.gd
# Сгенерировано BannerFlow Manager
# Шаблон: {template.name}
# Размер: {template.width}x{template.height}

extends Control

var player_data = {{
    "player_name": "Данные игрока",
    "score": 0,
    "level": 1
}}

func _ready():
    $Label.text = "Баннер: {banner_name}"
    update_display()

func update_display():
    $ScoreLabel.text = "Счет: " + str(player_data.score)
    $LevelLabel.text = "Уровень: " + str(player_data.level)

# HTML контент баннера:
# {html_content[:200]}...
"""
        return godot_script

    @staticmethod
    def parse_game_file(file_path):
        """
        Парсинг файла данных игры (JSON или CSV).

        :param file_path: str – путь к файлу
        :return: dict (для JSON) или list of dict (для CSV) при успехе, None при ошибке
        :raises ValueError: если формат файла не поддерживается
        """
        try:
            # Определяем формат по расширению
            if file_path.endswith('.json'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)

            elif file_path.endswith('.csv'):
                data = []
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        data.append(row)
                return data

            else:
                # Неподдерживаемый формат – выбрасываем исключение
                raise ValueError("Неподдерживаемый формат файла")

        except Exception as e:
            # Логируем ошибку (в реальном проекте лучше использовать logger)
            print(f"Ошибка парсинга файла: {e}")
            return None
