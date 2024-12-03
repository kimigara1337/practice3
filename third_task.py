import os
import json
from bs4 import BeautifulSoup
from collections import Counter
import statistics

# Функция для парсинга XML
def parse_xml(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "xml")  # используем xml парсер

    stars = []

    # Получаем информацию о звезде
    star_data = {}

    # Извлекаем данные для каждого элемента
    star_data["name"] = soup.find("name").text.strip()
    star_data["constellation"] = soup.find("constellation").text.strip()
    star_data["spectral_class"] = soup.find("spectral-class").text.strip()
    star_data["radius"] = float(soup.find("radius").text.strip())  # Преобразуем в число
    star_data["rotation"] = soup.find("rotation").text.strip()
    star_data["age"] = soup.find("age").text.strip()
    star_data["distance"] = float(soup.find("distance").text.strip().replace(" million km", "").strip())
    star_data["absolute_magnitude"] = float(soup.find("absolute-magnitude").text.strip().replace(" million km", "").strip())

    stars.append(star_data)

    return stars


# Получаем список всех XML файлов в директории
directory_path = "E:/66/lab3/task3"  # Путь к директории с файлами
xml_files = [f for f in os.listdir(directory_path) if f.endswith(".xml")]

# Парсим все XML файлы и собираем данные
all_stars = []
for file_name in xml_files:
    file_path = os.path.join(directory_path, file_name)
    stars = parse_xml(file_path)
    all_stars.extend(stars)

# 1. Сортировка данных по радиусу звезды (от большей к меньшей)
all_stars_sorted = sorted(all_stars, key=lambda x: x["radius"], reverse=True)  # Сортируем все звезды по радиусу

# 2. Фильтрация данных: звезды старше 3 миллиардов лет
filtered_stars = [
    star for star in all_stars
    if "billion years" in star["age"] and float(star["age"].split()[0]) > 3.0
]

# 3. Статистические характеристики для радиуса звезды
radii = [star["radius"] for star in all_stars]
total_radius = sum(radii)
min_radius = min(radii) if radii else 0
max_radius = max(radii) if radii else 0
average_radius = statistics.mean(radii) if radii else 0

# 4. Частота меток для созвездий
constellations = [star["constellation"] for star in all_stars]
constellation_counts = Counter(constellations)

# Подготовка данных для записи в JSON
output_data = {
    "all_stars": all_stars_sorted,  # Здесь все звезды отсортированы по радиусу
    "filtered_stars": filtered_stars,  # Звезды старше 3 миллиардов лет
    "statistics": {
        "total_radius": total_radius,
        "min_radius": min_radius,
        "max_radius": max_radius,
        "average_radius": average_radius
    },
    "constellation_frequency": constellation_counts  # Частота созвездий
}

# Запись данных в JSON
with open("third_task_stars_results.json", "w", encoding="utf-8") as json_file:
    json.dump(output_data, json_file, ensure_ascii=False, indent=4)

print("Данные успешно записаны в third_task_stars_results.json.")
