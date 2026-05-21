import random
import string
import requests
from data import *

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def register_new_user():
    """Регистрирует нового пользователя и возвращает (email, password, name, token)."""
    email = f"test_{generate_random_string()}@example.com"
    password = generate_random_string()
    name = f"User_{generate_random_string()}"
    payload = {"email": email, "password": password, "name": name}
    response = requests.post(REGISTER_URL, json=payload)
    if response.status_code == 200 and response.json().get("success"):
        token = response.json().get("accessToken")
        return email, password, name, token
    return None, None, None, None

def delete_user(token):
    """Удаляет пользователя по токену."""
    requests.delete(USER_URL, headers={"Authorization": token})

def get_ingredients():
    """Возвращает список ID ингредиентов."""
    resp = requests.get(INGREDIENTS_URL)
    if resp.status_code == 200:
        data = resp.json()
        return [item["_id"] for item in data.get("data", [])]
    return []

def get_random_ingredients(count=2):
    """Возвращает случайные ID ингредиентов."""
    all_ids = get_ingredients()
    if len(all_ids) >= count:
        return random.sample(all_ids, count)
    return all_ids
