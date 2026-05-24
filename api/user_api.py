import requests

from data import (
    REGISTER_URL,
    DELETE_USER_URL,
    LOGIN_URL,
    USER_URL
)


class UserApi:

    @staticmethod
    def create_user(payload):
        return requests.post(
            REGISTER_URL,
            json=payload
        )

    @staticmethod
    def login_user(payload):
        return requests.post(
            LOGIN_URL,
            json=payload
        )

    @staticmethod
    def update_user(payload, token):

        return requests.patch(
            USER_URL,
            json=payload,
            headers={"Authorization": token}
        )

    @staticmethod
    def delete_user(token):

        return requests.delete(
            DELETE_USER_URL,
            headers={"Authorization": token}
        )
