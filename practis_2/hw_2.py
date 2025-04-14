import requests
from bs4 import BeautifulSoup
import json
import re

# Список для хранения всех книг
all_books = []

# Базовый URL сайта
base_url = "http://books.toscrape.com/"


# Функция для получения данных о книгах с одной страницы
def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим все книги на странице
    books = soup.select('article.product_pod')

    for book in books:
        # Получаем ссылку на страницу книги
        book_url = base_url + book.find('h3').find('a')['href'].replace('../../../', 'catalogue/')

        # Переходим на страницу книги для получения подробной информации
        book_response = requests.get(book_url)
        book_response.encoding = 'utf-8'
        book_soup = BeautifulSoup(book_response.text, 'html.parser')

        # Извлекаем название
        title = book_soup.find('h1').text.strip()

        # Извлекаем цену
        price = float(book_soup.find('p', class_='price_color').text.replace('£', ''))

        # Извлекаем количество в наличии
        availability = book_soup.find('p', class_='instock availability').text.strip()
        # Используем регулярное выражение для извлечения числа
        stock = int(re.search(r'\d+', availability).group())

        # Извлекаем описание
        description_tag = book_soup.find('div', id='product_description')
        description = description_tag.find_next('p').text.strip() if description_tag else "No description available"

        # Добавляем информацию о книге в список
        all_books.append({
            'title': title,
            'price': price,
            'stock': stock,
            'description': description
        })


# Получаем все категории
response = requests.get(base_url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')
categories = soup.find('ul', class_='nav-list').find('ul').find_all('li')

# Проходим по всем категориям
for category in categories:
    category_url = base_url + category.find('a')['href']

    while category_url:
        # Скрейпим текущую страницу
        print(f"Scraping: {category_url}")
        scrape_page(category_url)

        # Проверяем наличие следующей страницы
        response = requests.get(category_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        next_button = soup.find('li', class_='next')

        if next_button:
            # Формируем URL следующей страницы
            next_page = next_button.find('a')['href']
            if next_page.startswith('page-'):
                category_url = category_url.rsplit('/', 1)[0] + '/' + next_page
            else:
                category_url = base_url + 'catalogue/' + next_page
        else:
            category_url = None

# Сохраняем данные в JSON-файл
with open('books_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_books, f, ensure_ascii=False, indent=4)

print(f"Сохранено {len(all_books)} книг в books_data.json")