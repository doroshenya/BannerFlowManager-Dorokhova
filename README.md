BannerFlow Manager
Веб-приложение для управления рекламными баннерами в играх.

Структура проекта BannerFlow_Manager  
bannerflow_app - основное приложение  
&emsp;migrations - Миграции базы данных  
&emsp;models.py - Модели Campaign и Banner  
&emsp;services.py - Бизнес-логика  
&emsp;urls.py - URL-ы приложения  
&emsp;views.py - Представления (home, api_banners)  
bannerflow_project - Настройки Django  
myenv - Виртуальное окружение Python  
db.sqlite3 - База данных SQLite  
manage.py - Django management script  
README.md - Документация  
requirements.txt - Зависимости Python  
my_django_env - Переменные окружения  

Быстрый старт
1. Активация виртуального окружения source myenv/bin/activate  
2. Установка зависимостей pip install -r requirements.txt  
3. Применение миграции базы данных python manage.py migrate  
4. Запуск сервера разработки python manage.py runserver  
5. Открытие в браузере http://127.0.0.1:8000/  

Модели данных  
Campaign (Кампании)  
&emsp;name - Название кампании  
&emsp;budget - Бюджет кампании  
&emsp;start_date - Дата начала  
&emsp;is_active - Статус активности  
Banner (Баннеры)  
&emsp;campaign - Связь с кампанией  
&emsp;image_url - URL изображения  
&emsp;title - Заголовок баннера  

Технологии  
Python 3.13  
Django 5.2.8  
SQLite  

UML диаграммы  
Use Case диаграмма  
<img width="425" height="451" alt="image" src="https://github.com/user-attachments/assets/1a94f0ff-bf68-4a4d-9ee2-e2bfdf01d6c5" />  

Deployment диаграмма  
<img width="412" height="423" alt="image" src="https://github.com/user-attachments/assets/35eef70d-e972-4886-b01d-dfc54e8bae37" />  
