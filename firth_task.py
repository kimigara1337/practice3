import os
import json
from bs4 import BeautifulSoup
import statistics
from collections import Counter

# Укажите путь к папке с HTML файлами
folder_path = 'E:/66/lab3/task1'  # Замените на ваш путь


# Функция для парсинга HTML
def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    data = {}

    # Извлечение типа турнира
    type_tag = soup.find('span')
    if type_tag:
        data['type'] = type_tag.text.split(': ')[1] if ': ' in type_tag.text else 'Unknown'

    # Извлечение названия турнира
    title_tag = soup.find('h1')
    if title_tag:
        title_text = title_tag.text
        if 'Турнир: ' in title_text:
            data['title'] = title_text.split('Турнир: ')[1]
        else:
            data['title'] = title_text.strip()  # Если формат другой, берем все содержимое

    # Извлечение города и даты начала
    address_tag = soup.find('p', class_='address-p')
    if address_tag:
        address_text = address_tag.text.split(' Начало: ')
        if len(address_text) > 1:
            data['city'] = address_text[0].split('Город: ')[1].strip() if 'Город: ' in address_text[0] else 'Unknown'
            data['start_date'] = address_text[1].strip()
        else:
            data['city'] = 'Unknown'
            data['start_date'] = 'Unknown'

    # Извлечение информации о турнире
    info_tag = soup.find_all('span')
    if len(info_tag) >= 3:
        data['rounds'] = int(info_tag[1].text.split(': ')[1]) if ': ' in info_tag[1].text else 0
        data['time_control'] = int(info_tag[2].text.split(': ')[1].split(' мин')[0]) if ': ' in info_tag[2].text else 0
        data['min_rating'] = int(info_tag[3].text.split(': ')[1]) if ': ' in info_tag[3].text else 0
    else:
        data['rounds'] = 0
        data['time_control'] = 0
        data['min_rating'] = 0

    # Извлечение рейтинга и просмотров
    rating_tag = soup.find_all('span')
    if len(rating_tag) > 4:
        data['rating'] = float(rating_tag[4].text.split(': ')[1]) if ': ' in rating_tag[4].text else 0.0
        data['views'] = int(rating_tag[5].text.split(': ')[1]) if ': ' in rating_tag[5].text else 0
    else:
        data['rating'] = 0.0
        data['views'] = 0

    # Извлечение ссылки на изображение
    img_tag = soup.find('img')
    data['image_url'] = img_tag['src'] if img_tag else 'No Image'

    return data


# Считываем все HTML файлы из папки
html_files = []
for filename in os.listdir(folder_path):
    if filename.endswith('.html'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            html_files.append(file.read())

# Преобразуем HTML в список словарей
tournaments = [parse_html(html) for html in html_files]

# Записываем данные в JSON
with open('tournaments.json', 'w', encoding='utf-8') as f:
    json.dump(tournaments, f, ensure_ascii=False, indent=4)

# 1. Сортировка по количеству туров
sorted_by_rounds = sorted(tournaments, key=lambda x: x['rounds'], reverse=True)
print("\nТурниры, отсортированные по количеству туров:")
print(json.dumps(sorted_by_rounds, ensure_ascii=False, indent=4))

# 2. Фильтрация по минимальному рейтингу
filtered_by_rating = [t for t in tournaments if t['min_rating'] > 2400]
print("\nТурниры с минимальным рейтингом выше 2400:")
print(json.dumps(filtered_by_rating, ensure_ascii=False, indent=4))

# 3. Статистические характеристики для просмотров
views = [t['views'] for t in tournaments]
views_sum = sum(views)
views_min = min(views)
views_max = max(views)
views_avg = statistics.mean(views)

print("\nСтатистические характеристики для просмотров:")
print(f"Сумма просмотров: {views_sum}")
print(f"Мин. просмотров: {views_min}")
print(f"Макс. просмотров: {views_max}")
print(f"Среднее количество просмотров: {views_avg}")

# 4. Частота типов турниров
type_counts = Counter([t['type'] for t in tournaments])
print("\nЧастота типов турниров:")
print(json.dumps(type_counts, ensure_ascii=False, indent=4))
