import requests

# Твой токен авторизации от Foursquare
api_key = "API_TOKEN"  # Замени на свой токен

# Конечная точка API
endpoint = "https://api.foursquare.com/v3/places/search"

# Запрос категории у пользователя
category = input("Введите категорию заведений (например, кофейни, музеи, парки): ")

# Запрос города у пользователя
city = input("Введите название города (например, Moscow): ")

# Параметры запроса
params = {
    "query": category,  # Категория для поиска
    "near": city,  # Город
    "limit": 10  # Ограничим до 10 результатов
}

# Заголовки с токеном авторизации
headers = {
    "Accept": "application/json",
    "Authorization": api_key
}

# Отправка GET-запроса
response = requests.get(endpoint, params=params, headers=headers)

# Проверка успешности запроса
if response.status_code == 200:
    print("Успешный запрос API!")
    data = response.json()
    venues = data["results"]

    # Вывод информации о заведениях
    for venue in venues:
        name = venue["name"]
        address = venue["location"].get("address", "Адрес не указан")
        rating = venue.get("rating", "Рейтинг не указан")  # Рейтинг может отсутствовать
        print(f"Название: {name}")
        print(f"Адрес: {address}")
        print(f"Рейтинг: {rating}")
        print("\n")
else:
    print("Запрос API завершился неудачей с кодом состояния:", response.status_code)
    print(response.text)