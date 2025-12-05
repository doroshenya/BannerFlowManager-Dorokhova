# banner_мой_игровой_баннер.gd
# Сгенерировано BannerFlow Manager
# Шаблон: Прогресс уровня
# Размер: 500x350

extends Control

var player_data = {
    "player_name": "Данные игрока",
    "score": 0,
    "level": 1
}

func _ready():
    $Label.text = "Баннер: Мой игровой баннер"
    update_display()

func update_display():
    $ScoreLabel.text = "Счет: " + str(player_data.score)
    $LevelLabel.text = "Уровень: " + str(player_data.level)

# HTML контент баннера:
# <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Баннер: Epic Adventure</title>
    <style>
    ...
