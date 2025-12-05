#!/bin/bash
echo "=== BannerFlow Manager Test Suite ==="

# Проверяем активацию виртуального окружения
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Активируем виртуальное окружение..."
    source myenv/bin/activate
fi

echo "Проверяем установку Django..."
python -c "import django; print(f'Django version: {django.__version__}')"

echo "Запускаем миграции..."
python manage.py migrate

echo "Запускаем проверку Django..."
python manage.py check

echo "Запускаем тесты через manage.py..."
python manage.py test bannerflow_app.tests -v 2

echo "=== Тестирование завершено ==="
