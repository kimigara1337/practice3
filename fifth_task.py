import requests
from bs4 import BeautifulSoup
import json
import statistics
from collections import Counter


# Функция для парсинга страницы, посвященной одному объекту
def parse_single_object_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Извлечение данных с учетом структуры страницы
    object_data = {
        "name": soup.find("h1").text.strip() if soup.find("h1") else None,
        "category": soup.find("span", {"class": "b-breadcrumbs__item"}).text.strip() if soup.find("span", {
            "class": "b-breadcrumbs__item"}) else None,
        "price": float(
            soup.find("span", {"class": "price__num"}).text.strip().replace("₽", "").replace(" ", "")) if soup.find(
            "span", {"class": "price__num"}) else None,
        "rating": float(soup.find("span", {"class": "product-ratings__rating"}).text.strip()) if soup.find("span", {
            "class": "product-ratings__rating"}) else None,
        "reviews": int(
            soup.find("span", {"class": "product-ratings__count"}).text.strip().replace("отзывы", "").replace("(",
                                                                                                              "").replace(
                ")", "").strip()) if soup.find("span", {"class": "product-ratings__count"}) else None
    }

    # Добавляем отладочный вывод, чтобы проверить данные
    print(f"Парсинг страницы: {url}")
    print(f"Название: {object_data['name']}")
    print(f"Категория: {object_data['category']}")
    print(f"Цена: {object_data['price']}")
    print(f"Рейтинг: {object_data['rating']}")
    print(f"Отзывы: {object_data['reviews']}")

    return object_data


# Пример URL страниц (замените на реальные URL)
single_object_urls = [
    "https://www.vseinstrumenti.ru/product/gantel-sbornaya-lite-weights-8-kg-h-1-sht-3108cd-4889748/",
    "https://www.vseinstrumenti.ru/product/razbornaya-gantel-urm-dlya-silovyh-trenirovok-24-kg-chernaya-b00145-7637937/",
    "https://www.vseinstrumenti.ru/product/reguliruemaya-gantel-gigant-40kg-proxima-ps-adb-5k-40k-13332871/",
    "https://www.vseinstrumenti.ru/product/ganteli-razbornye-s-grifom-urm-2-sht-h-15-kg-30-kg-b00203-1841906/",
    "https://www.vseinstrumenti.ru/product/razbornye-ganteli-s-grifom-urm-20-kg-2sht-h-10-kg-b00027-1561225/",
    "https://www.vseinstrumenti.ru/product/nabor-gantelej-i-shtanga-v-kejse-unixfit-50-kg-dbkitu50-5241955/",
    "https://www.vseinstrumenti.ru/product/razbornye-ganteli-s-grifom-urm-40-kg-2sht-h-20-kg-b00028-1561226/",
    "https://www.vseinstrumenti.ru/product/nabor-gantelej-bradex-20-kg-plastikovyj-kejs-sf-0557-1593115/",
    "https://www.vseinstrumenti.ru/product/gantel-reguliruemaya-bradex-24-kg-12-variantov-vesov-sf-1043-14046911/",
    "https://www.vseinstrumenti.ru/product/neoprenovaya-gantel-bradex-4-kg-fioletovaya-sf-0544-1593091/"
]  # URL страниц, посвященных отдельным объектам
catalog_urls = ["https://www.vseinstrumenti.ru/category/ganteli-169435/"]  # URL страницы каталога

# Спарсить страницы, посвященные одному объекту
single_objects_data = []
for url in single_object_urls:
    single_objects_data.append(parse_single_object_page(url))

# Спарсить страницы каталога (можно адаптировать по аналогии)
# catalog_data = []
# for url in catalog_urls:
#     catalog_data.extend(parse_catalog_page(url))

# Собираем все данные в один список
all_data = single_objects_data  # + catalog_data если есть страницы каталога

# 1. Сортировка по цене
sorted_by_price = sorted(all_data, key=lambda x: x["price"], reverse=True)

# 2. Фильтрация по рейтингу > 4
filtered_by_rating = [item for item in all_data if item["rating"] is not None and item["rating"] > 4]

# 3. Статистика для цены
prices = [item["price"] for item in all_data if item["price"] is not None]
sum_price = sum(prices)
min_price = min(prices) if prices else 0
max_price = max(prices) if prices else 0
mean_price = statistics.mean(prices) if prices else 0

# 4. Частота категорий
categories = [item["category"] for item in all_data if item["category"] is not None]
category_counts = Counter(categories)

# Сохраняем результаты в json
with open('single_objects_data.json', 'w', encoding='utf-8') as f:
    json.dump(single_objects_data, f, ensure_ascii=False, indent=4)

# Сохраняем результаты сортировки и фильтрации
with open('sorted_by_price.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_by_price, f, ensure_ascii=False, indent=4)

with open('filtered_by_rating.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_by_rating, f, ensure_ascii=False, indent=4)

# Печать статистики
print(f"Сумма цен: {sum_price}")
print(f"Минимальная цена: {min_price}")
print(f"Максимальная цена: {max_price}")
print(f"Средняя цена: {mean_price}")
print("\nЧастота категорий:")
for category, count in category_counts.items():
    print(f"{category}: {count}")
