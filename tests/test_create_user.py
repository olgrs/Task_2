import allure
import pytest
import requests
from data import REGISTER_URL
from helpers import register_new_user, delete_user, generate_random_string


class TestCreateUser:

    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user_success(self):
        email = f"test_{generate_random_string()}@example.com"
        password = generate_random_string()
        name = f"User_{generate_random_string()}"
        payload = {"email": email, "password": password, "name": name}
        response = requests.post(REGISTER_URL, json=payload)
        assert response.status_code == 200 and response.json()["success"] == True, (
            f"Ожидался статус 200 и success:true, получен статус {response.status_code}, тело: {response.text}"
        )
        # Удаляем созданного пользователя
        token = response.json().get("accessToken")
        if token:
            requests.delete(f"{REGISTER_URL}/user", headers={"Authorization": token})

    @allure.title("Создание уже зарегистрированного пользователя")
    def test_create_existing_user(self):
        email, password, name, token = register_new_user()
        assert token is not None, "Не удалось создать пользователя для подготовки теста"
        payload = {"email": email, "password": password, "name": name}
        response = requests.post(REGISTER_URL, json=payload)
        assert response.status_code == 403 and response.json()["success"] == False and "User already exists" in response.json()["message"], (
            f"Ожидалась ошибка 403, получен статус {response.status_code}, тело: {response.text}"
        )
        delete_user(token)

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, missing_field):
        payload = {"email": f"test_{generate_random_string()}@example.com", "password": generate_random_string(), "name": f"User_{generate_random_string()}"}
        del payload[missing_field]
        response = requests.post(REGISTER_URL, json=payload)
        assert response.status_code == 403 and response.json()["success"] == False and "required" in response.json()["message"].lower(), (
            f"Ожидалась ошибка 403 при отсутствии поля {missing_field}, получен статус {response.status_code}, тело: {response.text}"
        )

