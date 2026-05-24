import allure
import requests

from api.order_api import OrderApi
from data import ORDERS_URL
from helpers import get_random_ingredients


class TestGetUserOrders:

    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_with_auth(self, new_user):
        response_new_user, _ = new_user
        token = response_new_user.json()["accessToken"]
        ingredients = get_random_ingredients(2)
        payload = {"ingredients": [ingredients[0], ingredients[1]]}
        create_response = OrderApi.create_order(
            payload,
            token
        )
        response = OrderApi.get_user_orders(token)
        assert response.status_code == 200 
        assert response.json()["success"] == True 
        assert "orders" in response.json(), (
            f"Ожидался список заказов, статус {response.status_code}, тело: {response.text}"
        )

    @allure.title("Получение заказов без авторизации — ошибка")
    def test_get_orders_without_auth(self):
        response = requests.get(ORDERS_URL)
        assert response.status_code == 401
        assert response.json()["success"] == False
        assert "You should be authorised" in response.json()["message"], (
            f"Ожидалась ошибка авторизации, статус {response.status_code}, тело: {response.text}"
        )
