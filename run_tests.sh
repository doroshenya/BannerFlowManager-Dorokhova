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

echo "Запускаем тесты..."
pytest -v bannerflow_app/tests.py

echo "Проверяем покрытие кода..."
pytest --cov=bannerflow_app --cov-report=term-missing

echo "=== Тестирование завершено ==="
