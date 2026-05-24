import requests

from data import (
    REGISTER_URL,
    DELETE_USER_URL,
    LOGIN_URL,
    USER_URL
)


class UserApi:

    @allure.step("Создание пользователя")
    @staticmethod
    def create_user(payload):
        return requests.post(
            REGISTER_URL,
            json=payload
        )

    @allure.step("Логин пользователя")
    @staticmethod
    def login_user(payload):
        return requests.post(
            LOGIN_URL,
            json=payload
        )

    @allure.step("Обновление пользователя")
    @staticmethod
    def update_user(payload, token):
        return requests.patch(
            USER_URL,
            json=payload,
            headers={"Authorization": token}
        )

    @allure.step("Удаление пользователя")
    @staticmethod
    def delete_user(token):
        return requests.delete(
            DELETE_USER_URL,
            headers={"Authorization": token}
        )
