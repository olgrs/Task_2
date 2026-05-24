import allure
import requests

from api.order_api import OrderApi
from data import ORDERS_URL
from helpers import get_random_ingredients


class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и валидными ингредиентами")
    def test_create_order_with_auth_valid_ingredients(self, new_user):
        response_new_user, _ = new_user
        token = response_new_user.json()["accessToken"]
        ingredients = get_random_ingredients(2)
        payload = {"ingredients": [ingredients[0], ingredients[1]]}
        response = OrderApi.create_order(
            payload,
            token
        )
        assert response.status_code == 200
        assert response.json()["success"] == True
        assert "order" in response.json(), (
            f"Ожидался успешный заказ, статус {response.status_code}, тело: {response.text}"
        )

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self):
        ingredients = get_random_ingredients(2)
        payload = {"ingredients": [ingredients[0], ingredients[1]]}
        response = requests.post(ORDERS_URL, json=payload)
        assert response.status_code == 200
        assert response.json()["success"] == True
        assert "order" in response.json(), (
            f"Ожидался успешный заказ, статус {response.status_code}, тело: {response.text}"
        )

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_empty_ingredients(self):
        payload = {"ingredients": []}
        response = requests.post(ORDERS_URL, json=payload)
        assert response.status_code == 400
        assert response.json()["success"] == False
        assert "Ingredient ids must be provided" in response.json()["message"], (
            f"Ожидалась ошибка 400, статус {response.status_code}, тело: {response.text}"
        )

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_hash(self):
        payload = {"ingredients": ["invalid_hash_123"]}
        response = requests.post(ORDERS_URL, json=payload)
        assert response.status_code == 500, (
            f"Ожидался статус 500, получен {response.status_code}, тело: {response.text}"
        )
