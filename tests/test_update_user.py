import allure
import pytest
import requests

from api.user_api import UserApi
from data import USER_URL
from helpers import generate_random_string


class TestUpdateUser:

    @allure.title("Изменение данных авторизованного пользователя: поле {field}")
    @pytest.mark.parametrize("field, new_value", [
        ("email", f"updated_{generate_random_string()}@example.com"),
        ("password", generate_random_string()),
        ("name", f"UpdatedName_{generate_random_string()}")
    ])
    def test_update_user_with_auth(self, new_user, field, new_value):
        response_create_user, _ = new_user
        token = response_create_user.json()["accessToken"]
        payload = {field: new_value}
        response = UserApi.update_user(payload, token)
        assert response.status_code == 200 
        assert response.json()["success"] == True, (
            f"Ожидался статус 200 и success:true при изменении {field}, "
            f"получен статус {response.status_code}, тело: {response.text}"
        )

    @allure.title("Изменение данных без авторизации — ошибка")
    @pytest.mark.parametrize("field, new_value", [
        ("email", f"updated_{generate_random_string()}@example.com"),
        ("password", generate_random_string()),
        ("name", f"UpdatedName_{generate_random_string()}")
    ])
    def test_update_user_without_auth(self, field, new_value):
        payload = {field: new_value}
        response = requests.patch(USER_URL, json=payload)
        assert response.status_code == 401
        assert response.json()["success"] == False
        assert "You should be authorised" in response.json()["message"], (
            f"Ожидалась ошибка 401, получен статус {response.status_code}, тело: {response.text}"
        )
