import requests

from data import ORDERS_URL


class OrderApi:

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

    @staticmethod
    def get_user_orders(token):

        return requests.get(
            ORDERS_URL,
            headers={"Authorization": token}
        )
