import allure
import pytest
import requests

from data import REGISTER_URL
from helpers import generate_random_string


class TestCreateUser:

    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user_success(self, user_data):
        response = requests.post(REGISTER_URL, json=user_data)
        assert response.status_code == 200
        assert response.json()["success"] is True, (
            f"Ожидался success=True, получено: {response.json()}"
        )

    @allure.title("Создание уже зарегистрированного пользователя")
    def test_create_existing_user(
            self,
            new_user
    ):

        _, user_data = new_user

        payload = {
            "email": user_data["email"],
            "password": user_data["password"],
            "name": user_data["name"]
        }

        response = requests.post(
            REGISTER_URL,
            json=payload
        )
        assert response.status_code == 403 
        assert response.json()["success"] == False 
        assert "User already exists" in response.json()["message"], (
            f"Ожидалась ошибка 403, получен статус {response.status_code}, тело: {response.text}"
        )

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, missing_field):
        payload = {
            "email": f"test_{generate_random_string()}@example.com",
            "password": generate_random_string(),
            "name": f"User_{generate_random_string()}"
        }
        del payload[missing_field]
        response = requests.post(REGISTER_URL, json=payload)
        assert response.status_code == 403 
        assert response.json()["success"] == False 
        assert "required" in response.json()["message"].lower(), (
            f"Ожидалась ошибка 403 при отсутствии поля {missing_field}, получен статус {response.status_code}, тело: {response.text}"
        )
