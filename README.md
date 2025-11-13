BannerFlow Manager
Веб-приложение для управления рекламными баннерами в играх.

Структура проекта
BannerFlow_Manager  
  &emsp;bannerflow_app - основное приложение  
      &emsp;&emsp;migrations - Миграции базы данных  
      &emsp;&emsp;models.py - Модели Campaign и Banner  
      &emsp;&emsp;services.py - Бизнес-логика  
      &emsp;&emsp;urls.py - URL-ы приложения  
      &emsp;&emsp;views.py - Представления (home, api_banners)  
  &emsp;bannerflow_project - Настройки Django  
  &emsp;myenv - Виртуальное окружение Python  
  &emsp;db.sqlite3 - База данных SQLite  
  &emsp;manage.py - Django management script  
  &emsp;README.md - Документация  
  &emsp;requirements.txt - Зависимости Python  
  &emsp;my_django_env - Переменные окружения  

Быстрый старт
1. Активация виртуального окружения source myenv/bin/activate
2. Установка зависимостей pip install -r requirements.txt
3. Применение миграции базы данных python manage.py migrate
4. Запуск сервера разработки python manage.py runserver
5. Открытие в браузере http://127.0.0.1:8000/

Модели данных

Campaign (Кампании)
  name - Название кампании
  budget - Бюджет кампании
  start_date - Дата начала
  is_active - Статус активности
Banner (Баннеры)
  campaign - Связь с кампанией
  image_url - URL изображения
  title - Заголовок баннера

Технологии
Python 3.13
Django 5.2.8
SQLite

UML диаграммы
Use Case диаграмма
<img width="425" height="451" alt="image" src="https://github.com/user-attachments/assets/1a94f0ff-bf68-4a4d-9ee2-e2bfdf01d6c5" />

Deployment диаграмма
<img width="412" height="423" alt="image" src="https://github.com/user-attachments/assets/35eef70d-e972-4886-b01d-dfc54e8bae37" />
