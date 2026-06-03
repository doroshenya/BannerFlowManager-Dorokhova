from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
import tempfile
import os
import atexit

# Импорт моделей (будем импортировать внутри функций при необходимости)

def home(request):
    """Домашняя страница."""
    return render(request, 'bannerflow_app/home.html')

def dashboard(request):
    """Панель управления (дашборд)."""
    return render(request, 'bannerflow_app/dashboard.html')


# ===== ГЕНЕРАТОР БАННЕРОВ =====

def banner_generator(request):
    """
    Главная страница генератора баннеров.
    Отображает список доступных шаблонов и загруженных игровых данных.
    """
    try:
        from .models import BannerTemplate, GameData
        templates = BannerTemplate.objects.all()
        game_data = GameData.objects.all()

        return render(request, 'bannerflow_app/banner_generator.html', {
            'templates': templates,
            'game_data': game_data,
        })
    except Exception as e:
        # При ошибке отдаём пустые списки и сообщение об ошибке
        return render(request, 'bannerflow_app/banner_generator.html', {
            'templates': [],
            'game_data': [],
            'error': str(e)
        })

def generate_banner(request):
    """
    Обработка POST-запроса на генерацию баннера.
    Создаёт запись GeneratedBanner, генерирует HTML и экспорт для Godot,
    сохраняет файл .gd и перенаправляет на страницу предпросмотра.
    """
    if request.method == 'POST':
        try:
            from .models import BannerTemplate, GameData, GeneratedBanner
            from .banner_generator import BannerGenerator

            template_id = request.POST.get('template')
            game_data_id = request.POST.get('game_data')
            banner_name = request.POST.get('name', 'Новый баннер')

            template = BannerTemplate.objects.get(id=template_id)
            game_data = GameData.objects.get(id=game_data_id)

            # Генерируем HTML-код баннера
            html_content = BannerGenerator.generate_html(template, game_data)

            # Генерируем GDScript для Godot
            godot_script = BannerGenerator.export_for_godot(
                html_content,
                banner_name,
                template
            )

            # Создаём запись в БД
            banner = GeneratedBanner.objects.create(
                name=banner_name,
                template=template,
                game_data=game_data,
                html_content=html_content,
            )

            # Сохраняем .gd файл во временный файл, затем в поле модели
            with tempfile.NamedTemporaryFile(mode='w', suffix='.gd', delete=False, encoding='utf-8') as f:
                f.write(godot_script)
                temp_path = f.name

            with open(temp_path, 'rb') as f:
                from django.core.files import File
                banner.godot_export.save(f'banner_{banner.id}.gd', File(f))

            # Удаляем временный файл
            os.unlink(temp_path)

            messages.success(request, f'Баннер "{banner_name}" успешно создан!')
            return redirect('banner_preview', banner_id=banner.id)

        except Exception as e:
            messages.error(request, f'Ошибка генерации: {str(e)}')
            return redirect('banner_generator')

    return redirect('banner_generator')


def banner_preview(request, banner_id):
    """
    Страница предпросмотра сгенерированного баннера.
    Показывает HTML-контент баннера и информацию о нём.
    """
    try:
        from .models import GeneratedBanner
        banner = GeneratedBanner.objects.get(id=banner_id)

        return render(request, 'bannerflow_app/banner_preview.html', {
            'banner': banner
        })
    except Exception as e:
        return HttpResponse(f'<h1>Ошибка:</h1><p>{str(e)}</p>')


def export_banner(request, banner_id):
    """
    Экспорт баннера для Godot Engine.
    Генерирует .gd файл на лету и отдаёт его на скачивание.
    """
    try:
        from .models import GeneratedBanner
        from .banner_generator import BannerGenerator

        banner = GeneratedBanner.objects.get(id=banner_id)

        # Генерируем скрипт для Godot
        godot_script = BannerGenerator.export_for_godot(
            banner.html_content,
            banner.name,
            banner.template
        )

        # Создаём временный файл с расширением .gd
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.gd',
            delete=False,
            encoding='utf-8'
        ) as temp_file:
            temp_file.write(godot_script)
            temp_path = temp_file.name

        filename = f"banner_{banner.id}.gd"

        # Отправляем файл на скачивание
        response = FileResponse(
            open(temp_path, 'rb'),
            as_attachment=True,
            filename=filename,
            content_type='text/plain'
        )

        # Удаляем временный файл после отправки
        def cleanup():
            try:
                os.unlink(temp_path)
            except:
                pass
        atexit.register(cleanup)

        return response

    except GeneratedBanner.DoesNotExist:
        return HttpResponse("Баннер не найден", status=404)
    except Exception as e:
        return HttpResponse(f'Ошибка экспорта: {str(e)}', status=500)


def banner_list(request):
    """
    Страница со списком всех сгенерированных баннеров.
    Используется для выбора баннера перед экспортом.
    """
    from .models import GeneratedBanner
    banners = GeneratedBanner.objects.all().order_by('-created_at')
    return render(request, 'bannerflow_app/banner_list.html', {
        'banners': banners
    })


def api_banners(request):
    """
    API-эндпоинт для получения списка активных баннеров.
    Возвращает JSON-список баннеров из активных кампаний.
    """
    try:
        from .models import Campaign
        campaigns = Campaign.objects.filter(status='active')

        banners_data = []
        for campaign in campaigns:
            for banner in campaign.banners.all():
                banners_data.append({
                    'id': banner.id,
                    'title': banner.title,
                    'campaign': campaign.name,
                    'status': campaign.status,
                })

        return JsonResponse({'banners': banners_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def upload_game_data(request):
    """
    Страница загрузки данных игры (JSON/CSV).
    """
    return render(request, 'bannerflow_app/upload_game_data.html')