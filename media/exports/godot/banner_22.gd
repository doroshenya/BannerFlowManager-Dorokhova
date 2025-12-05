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
    print("Баннер загружен в Godot")

func update_display():
    $ScoreLabel.text = "Счет: " + str(player_data.score)
    $LevelLabel.text = "Уровень: " + str(player_data.level)
