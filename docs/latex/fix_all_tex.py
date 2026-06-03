import os
import re

# Функция для замены кириллицы
def replace_cyrillic(text):
    # Заменяем все русские буквы на латинские аналоги или удаляем
    cyr_to_lat = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
        'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch',
        'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D',
        'Е': 'E', 'Ё': 'E', 'Ж': 'Zh', 'З': 'Z', 'И': 'I',
        'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
        'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T',
        'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch',
        'Ш': 'Sh', 'Щ': 'Shch', 'Ъ': '', 'Ы': 'Y', 'Ь': '',
        'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
    }
    
    # Заменяем по словарю
    for cyr, lat in cyr_to_lat.items():
        text = text.replace(cyr, lat)
    
    # Заменяем box-drawing символы
    box_chars = {'└': '|-', '─': '-', '├': '|', '┘': '|_', 
                 '┌': '|_', '┐': '_|', '┤': '|', '┬': '|-',
                 '┴': '-|', '│': '|'}
    for char, replacement in box_chars.items():
        text = text.replace(char, replacement)
    
    return text

# Обрабатываем все .tex файлы
for filename in os.listdir('.'):
    if filename.endswith('.tex'):
        print(f'Processing {filename}...')
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        new_content = replace_cyrillic(content)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f'  {filename} fixed')

print('All files processed!')
