import os
import json
from bs4 import BeautifulSoup
import statistics
from collections import Counter
import re

# Путь к папке с HTML файлами
folder_path = 'E:/66/lab3/task2'  # Замените на ваш путь


# Функция для парсинга одного товара
def parse_product(product):
    data = {}

    # Название товара
    name_tag = product.find('span')
    data['name'] = name_tag.text.strip() if name_tag else "Unknown"

    # Цена товара
    price_tag = product.find('price')
    if price_tag:
        data['price'] = int(price_tag.text.strip().replace('₽', '').replace(' ', ''))
    else:
        data['price'] = None

    # Бонусы (извлекаем только цифры)
    bonus_tag = product.find('strong')
    if bonus_tag:
        bonus_text = bonus_tag.text.strip()
        bonus_value = re.findall(r'\d+', bonus_text)  # Ищем все числа в строке
        data['bonus'] = int(bonus_value[0]) if bonus_value else None
    else:
        data['bonus'] = None

    # Характеристики товара (например, процессор, камера)
    characteristics = {}
    for li in product.find_all('li'):
        char_type = li.get('type', 'Unknown')
        characteristics[char_type] = li.text.strip()

    data['characteristics'] = characteristics

    return data


# Считываем все HTML файлы из папки
html_files = []
for filename in os.listdir(folder_path):
    if filename.endswith('.html'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            html_files.append(file.read())

# Преобразуем HTML в список товаров
products = []
for html in html_files:
    soup = BeautifulSoup(html, 'html.parser')
    product_items = soup.find_all('div', class_='product-item')
    for product in product_items:
        product_data = parse_product(product)
        products.append(product_data)

# Записываем данные в JSON
with open('products.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=4)

# Проверка, что товары действительно были собраны
if not products:
    print("Не удалось собрать товары. Проверьте HTML файлы.")
else:
    # 1. Сортировка по цене (от самой дешевой к самой дорогой)
    sorted_by_price = sorted(products, key=lambda x: x['price'] if x['price'] else float('inf'))
    print("\nТовары, отсортированные по цене:")
    print(json.dumps(sorted_by_price, ensure_ascii=False, indent=4))

    # 2. Фильтрация по наличию AMOLED-матрицы
    filter_amoled = [p for p in products if 'AMOLED' in p['characteristics'].values()]
    print("\nТовары с AMOLED-матрицей:")
    print(json.dumps(filter_amoled, ensure_ascii=False, indent=4))

    # 3. Статистические характеристики для цены
    prices = [p['price'] for p in products if p['price']]
    if prices:  # Проверяем, не пустой ли список
        price_sum = sum(prices)
        price_min = min(prices)
        price_max = max(prices)
        price_avg = statistics.mean(prices)

        print("\nСтатистические характеристики для цены:")
        print(f"Сумма цен: {price_sum}")
        print(f"Мин. цена: {price_min}")
        print(f"Макс. цена: {price_max}")
        print(f"Средняя цена: {price_avg}")
    else:
        print("\nНет данных для статистики по цене.")

    # 4. Частота характеристик типа "camera"
    camera_counts = Counter([p['characteristics'].get('camera', 'Unknown') for p in products])
    print("\nЧастота характеристик по камере:")
    print(json.dumps(camera_counts, ensure_ascii=False, indent=4))
