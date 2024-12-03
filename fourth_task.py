import os
import xml.etree.ElementTree as ET
import json
from collections import Counter
import statistics


# Функция для парсинга XML файла
def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    clothing_items = []

    for item in root.findall("clothing"):
        clothing_data = {
            "id": int(item.find("id").text.strip()) if item.find("id") is not None else None,
            "name": item.find("name").text.strip() if item.find("name") is not None else None,
            "category": item.find("category").text.strip() if item.find("category") is not None else None,
            "size": item.find("size").text.strip() if item.find("size") is not None else None,
            "color": item.find("color").text.strip() if item.find("color") is not None else None,
            "material": item.find("material").text.strip() if item.find("material") is not None else None,
            "price": float(item.find("price").text.strip()) if item.find("price") is not None else None,
            "rating": float(item.find("rating").text.strip()) if item.find("rating") is not None else None,
            "reviews": int(item.find("reviews").text.strip()) if item.find("reviews") is not None else None
        }
        # Добавляем необязательные поля, если они присутствуют
        for optional_field in ["new", "exclusive", "sporty"]:
            field_value = item.find(optional_field)
            clothing_data[optional_field] = field_value.text.strip() if field_value is not None else None

        clothing_items.append(clothing_data)

    return clothing_items


# Путь к папке с файлами
directory_path = "E:/66/lab3/task4"  # Укажите путь к своей папке с XML файлами

# Получаем список всех XML файлов в указанной папке
file_paths = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith(".xml")]

# Парсим все файлы
all_clothing_items = []
for path in file_paths:
    all_clothing_items.extend(parse_xml(path))

# Сохранение данных в JSON
with open('clothing_items.json', 'w', encoding='utf-8') as json_file:
    json.dump(all_clothing_items, json_file, ensure_ascii=False, indent=4)

# 1. Сортировка по цене (по убыванию)
sorted_by_price = sorted(all_clothing_items, key=lambda x: x["price"], reverse=True)

# 2. Фильтрация: объекты с рейтингом > 4
filtered_by_rating = [item for item in all_clothing_items if item["rating"] > 4]

# 3. Статистика для цены (сумма, мин, макс, среднее)
prices = [item["price"] for item in all_clothing_items if item["price"] is not None]
sum_price = sum(prices)
min_price = min(prices) if prices else 0
max_price = max(prices) if prices else 0
mean_price = statistics.mean(prices) if prices else 0

# 4. Частота для категории (category)
categories = [item["category"] for item in all_clothing_items if item["category"] is not None]
category_counts = Counter(categories)

# Результаты статистики
print(f"Сумма цен: {sum_price}")
print(f"Минимальная цена: {min_price}")
print(f"Максимальная цена: {max_price}")
print(f"Средняя цена: {mean_price}")

print("\nЧастота категорий:")
for category, count in category_counts.items():
    print(f"{category}: {count}")

# Сохранение результатов
with open('sorted_by_price.json', 'w', encoding='utf-8') as file:
    json.dump(sorted_by_price, file, ensure_ascii=False, indent=4)

with open('filtered_by_rating.json', 'w', encoding='utf-8') as file:
    json.dump(filtered_by_rating, file, ensure_ascii=False, indent=4)
