import allure
import pytest
import requests
from data import USER_URL
from helpers import register_new_user, delete_user, generate_random_string


class TestUpdateUser:

    @allure.title("Изменение данных авторизованного пользователя: поле {field}")
    @pytest.mark.parametrize("field, new_value", [
        ("email", f"updated_{generate_random_string()}@example.com"),
        ("password", generate_random_string()),
        ("name", f"UpdatedName_{generate_random_string()}")
    ])
    def test_update_user_with_auth(self, field, new_value):
        # Создаем пользователя
        email, password, name, token = register_new_user()
        assert token is not None
        # Формируем тело для обновления
        payload = {field: new_value}
        # Отправляем запрос с авторизацией
        response = requests.patch(USER_URL, json=payload, headers={"Authorization": token})
        assert response.status_code == 200 and response.json()["success"] == True, (
            f"Ожидался статус 200 и success:true при изменении {field}, "
            f"получен статус {response.status_code}, тело: {response.text}"
        )
        # Удаляем пользователя (токен остался валидным)
        delete_user(token)

    @allure.title("Изменение данных без авторизации — ошибка")
    def test_update_user_without_auth(self):
        # Создаем пользователя, чтобы убедиться, что он существует
        email, password, name, token = register_new_user()
        assert token is not None
        # Пытаемся изменить без токена
        payload = {"name": "NoAuthName"}
        response = requests.patch(USER_URL, json=payload)
        assert response.status_code in [401, 403] and response.json()["success"] == False, (
            f"Ожидалась ошибка 401/403, получен статус {response.status_code}, тело: {response.text}"
        )
        # Удаляем пользователя
        delete_user(token)