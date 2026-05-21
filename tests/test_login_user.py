import allure
import pytest
import requests
from data import LOGIN_URL
from helpers import register_new_user, delete_user, generate_random_string


class TestLoginUser:

    @allure.title("Успешный логин существующего пользователя")
    def test_login_success(self):
        email, password, name, token = register_new_user()
        assert token is not None
        payload = {"email": email, "password": password}
        response = requests.post(LOGIN_URL, json=payload)
        assert response.status_code == 200 and response.json()["success"] == True and "accessToken" in response.json(), (
            f"Ожидался успешный вход, статус {response.status_code}, тело: {response.text}"
        )
        delete_user(token)

    @allure.title("Логин с неверным логином")
    def test_login_invalid_email(self):
        email, password, name, token = register_new_user()
        assert token is not None
        payload = {"email": "wrong_" + email, "password": password}
        response = requests.post(LOGIN_URL, json=payload)
        assert response.status_code == 401 and response.json()["success"] == False and "email or password" in response.json()["message"].lower(), (
            f"Ожидалась ошибка 401, получен статус {response.status_code}, тело: {response.text}"
        )
        delete_user(token)

    @allure.title("Логин с неверным паролем")
    def test_login_invalid_password(self):
        email, password, name, token = register_new_user()
        assert token is not None
        payload = {"email": email, "password": "wrong_" + password}
        response = requests.post(LOGIN_URL, json=payload)
        assert response.status_code == 401 and response.json()["success"] == False and "email or password" in response.json()["message"].lower(), (
            f"Ожидалась ошибка 401, получен статус {response.status_code}, тело: {response.text}"
        )
        delete_user(token)

        