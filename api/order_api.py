import requests

from data import ORDERS_URL


class OrderApi:

    @allure.step("Создание заказа")
    @staticmethod
    def create_order(payload, token=None):
        headers = {}
        if token:
            headers["Authorization"] = token
        return requests.post(
            ORDERS_URL,
            json=payload,
            headers=headers
        )

    @allure.step("Получение списка заказов пользователя")
    @staticmethod
    def get_user_orders(token):
        return requests.get(
            ORDERS_URL,
            headers={"Authorization": token}
        )
