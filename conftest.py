import pytest
import requests

from data import REGISTER_URL, DELETE_USER_URL
from helpers import generate_random_string


@pytest.fixture
def new_user():
    """
    Создаёт нового пользователя через API.
    Возвращает кортеж (response, user_data, token).
    После теста удаляет пользователя, если он был создан.
    """
    email = f"test_{generate_random_string()}@example.com"
    password = generate_random_string()
    name = f"User_{generate_random_string()}"
    payload = {"email": email, "password": password, "name": name}
    response = requests.post(REGISTER_URL, json=payload)

    token = None
    if response.status_code == 200 and response.json().get("success"):
        token = response.json().get("accessToken")

    user_data = {"email": email, "password": password, "name": name}

    yield response, user_data, token

    if token:
        requests.delete(DELETE_USER_URL, headers={"Authorization": token})

@pytest.fixture
def auth_token(new_user):
    """
    Возвращает токен авторизации созданного пользователя.
    Если создание не удалось, токен будет None.
    """
    _, _, token = new_user
    return token

@pytest.fixture
def user_data(new_user):
    """
    Возвращает словарь с данными созданного пользователя (email, password, name).
    """
    _, data, _ = new_user
    return data

@pytest.fixture
def user_data_before_registration():
    email = f"test_{generate_random_string()}@example.com"
    password = generate_random_string()
    name = f"User_{generate_random_string()}"
    user_data = {"email": email, "password": password, "name": name}
    return user_data
