import requests
from bs4 import BeautifulSoup
import time


def find_word_in_workshop(target_word):
    # ID игры Everlasting Summer на Steam
    steam_app_id = "331470"

    # Формируем URL для запроса к мастерской Steam для игры Everlasting Summer
    url = f"https://steamcommunity.com/app/{steam_app_id}/workshop/?section=items"

    # Отправляем GET-запрос и получаем HTML-код страницы
    response = requests.get(url)

    # Проверяем успешность запроса
    if response.status_code != 200:
        print("Ошибка при получении страницы")
        return

    # Создаем объект BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Находим все элементы с описаниями работ
    work_items = soup.find_all(class_="workshopItem")

    # Перебираем найденные работы
    for item in work_items:
        # Проверяем, является ли элемент работой (не коллекцией)
        if not item.find(class_="collectionIcon"):
            # Получаем описание работы
            description = item.find(class_="workshopItemDescription").get_text()
            # Проверяем наличие целевого слова в описании
            if target_word.lower() in description.lower().split():
                # Разбиваем описание на слова
                words = description.split()
                # Находим индекс целевого слова
                target_index = words.index(target_word.lower())
                # Выводим контекст (10 слов до и после целевого слова)
                context_start = max(0, target_index - 10)
                context_end = min(len(words), target_index + 11)
                context = ' '.join(words[context_start:context_end])
                print("Контекст:")
                print(context)
                # Получаем ссылку на работу
                workshop_link = item.find("a", class_="ugc")["href"]
                print("Ссылка на работу:", workshop_link)
                print()
                # Если слово найдено, прерываем поиск и возвращаемся
                return

    print("Слово не найдено в описаниях работ")


# Пример использования
target_word = "да"
find_word_in_workshop(target_word)
