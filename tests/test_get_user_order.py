import allure
import pytest
import requests
from data import ORDERS_URL
from helpers import get_random_ingredients


class TestGetUserOrders:

    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_with_auth(self, auth_token):
        # Сначала создадим заказ
        ingredients = get_random_ingredients(2)
        payload = {"ingredients": [ingredients[0], ingredients[1]]}
        requests.post(ORDERS_URL, json=payload, headers={"Authorization": auth_token})

        response = requests.get(ORDERS_URL, headers={"Authorization": auth_token})
        assert response.status_code == 200 and response.json()["success"] == True and "orders" in response.json(), (
            f"Ожидался список заказов, статус {response.status_code}, тело: {response.text}"
        )
        assert response.json()["total"] > 0 or response.json()["totalToday"] >= 0, (
            "Ответ не содержит ожидаемые поля 'total' или 'totalToday'"
        )

    @allure.title("Получение заказов без авторизации — ошибка")
    def test_get_orders_without_auth(self):
        response = requests.get(ORDERS_URL)
        assert response.status_code in [401, 403] and response.json()["success"] == False, (
            f"Ожидалась ошибка авторизации, статус {response.status_code}, тело: {response.text}"
        )