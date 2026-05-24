import allure
import random
import string
import requests

from data import *

@allure.step("Генерация рандомной строки")
def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

@allure.step("Получение списка ингредиентов")
def get_ingredients():
    """Возвращает список ID ингредиентов."""
    resp = requests.get(INGREDIENTS_URL)
    if resp.status_code == 200:
        data = resp.json()
        return [item["_id"] for item in data.get("data", [])]
    return []

@allure.step("Получение списка случайных ингредиентов")
def get_random_ingredients(count=2):
    """Возвращает случайные ID ингредиентов."""
    all_ids = get_ingredients()
    if len(all_ids) >= count:
        return random.sample(all_ids, count)
    return all_ids
