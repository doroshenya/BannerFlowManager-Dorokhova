# Добавим JavaScript функцию в конец шаблона
cat >> bannerflow_app/templates/bannerflow_app/banner_preview_final.html << 'JS'

<script>
// Функция для принудительного скачивания с правильным именем
function downloadGodotExport(bannerId, bannerName) {
    // Создаем безопасное имя файла
    let safeName = bannerName.replace(/[^a-zA-Z0-9а-яА-Я\s]/g, '').replace(/\s+/g, '_');
    let filename = `banner_${safeName}.gd`;
    
    // Создаем ссылку для скачивания
    let link = document.createElement('a');
    link.href = `/banner/export/${bannerId}/`;
    link.download = filename;
    link.target = '_blank';
    
    // Имитируем клик
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
</script>
JS

echo "✓ JavaScript функция добавлена"
