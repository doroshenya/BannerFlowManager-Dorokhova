BannerFlow Manager
Веб-приложение для управления рекламными баннерами в играх с генерацией кода для Godot Engine.

Быстрый старт
Активация виртуального окружения
source myenv/bin/activate

Установка зависимостей
pip install -r requirements.txt

Настройка базы данных
python manage.py migrate

Запуск сервера
python manage.py runserver
Откройте в браузере: http://127.0.0.1:8000/

Структура проекта  
bannerflow_app/          # Основное приложение Django  
├── migrations/          # Миграции БД  
├── models.py           # Модели данных  
├── views.py            # Контроллеры  
├── services.py         # Бизнес-логика  
├── banner_generator.py # Генератор баннеров  
└── data_parser.py      # Парсер CSV/XLSX  

bannerflow_project/     # Настройки проекта  
├── settings.py         # Конфигурация  
└── urls.py             # URL маршруты  

docs/                   # Документация  
├── html/              # Doxygen HTML  
└── pdf_output/        # PDF документация  

media/                  # Медиафайлы  
├── banners/           # Сгенерированные баннеры  
└── exports/godot/     # Скрипты для Godot  

.gitignore             # Игнорируемые файлы  
requirements.txt       # Зависимости Python  
manage.py             # Django скрипт  
pytest.ini           # Конфигурация тестов  
doxygen.config       # Конфигурация Doxygen  
Основные возможности
Парсинг игровых данных - загрузка CSV/XLSX файлов
Генерация баннеров - создание рекламных баннеров
Экспорт в Godot - автоматическая генерация .gd скриптов
A/B тестирование - сравнение эффективности баннеров
Полная документация - Doxygen + LaTeX

Модели данных
Campaign - Рекламные кампании
Banner - Баннеры
BannerTemplate - Шаблоны баннеров
GameData - Игровые данные
ABTest - A/B тесты
GeneratedBanner - Сгенерированные баннеры

Тестирование
# Запуск всех тестов
./run_tests.sh

Запуск с покрытием
pytest --cov=bannerflow_app tests/

Документация
Генерация HTML документации
doxygen doxygen.config
Файлы доступны в docs/html/

Технологии
Python 3.13 + Django 5.2.8
SQLite - база данных
Pillow - обработка изображений
pandas - анализ данных
Doxygen - документация
pytest - тестирование

UML диаграммы  
Use Case диаграмма  
<img width="1020" height="413" alt="image" src="https://github.com/user-attachments/assets/6cceb00f-b83b-452c-9a72-87b06852bb85" />
 

Deployment диаграмма  
<img width="412" height="423" alt="image" src="https://github.com/user-attachments/assets/35eef70d-e972-4886-b01d-dfc54e8bae37" />  
