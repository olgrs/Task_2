import allure
import requests

from data import LOGIN_URL


class TestLoginUser:

    @allure.title("Успешный логин существующего пользователя")
    def test_login_success(self, new_user):
        _, user_data = new_user
        payload = {"email": user_data["email"], "password": user_data["password"]}
        response = requests.post(LOGIN_URL, json=payload)
        assert response.status_code == 200 
        assert response.json()["success"] == True 
        assert "accessToken" in response.json(), (
            f"Ожидался успешный вход, статус {response.status_code}, тело: {response.text}"
        )

    @allure.title("Логин с неверным логином")
    def test_login_invalid_email(self, user_data):
        payload = {"email": "wrong_" + user_data["email"], "password": user_data["password"]}
        response = requests.post(LOGIN_URL, json=payload)
        assert response.status_code == 401 
        assert response.json()["success"] == False
        assert "email or password" in response.json()["message"].lower(), (
            f"Ожидалась ошибка 401, получен статус {response.status_code}, тело: {response.text}"
        )

    @allure.title("Логин с неверным паролем")
    def test_login_invalid_password(self, user_data):
        payload = {"email": user_data["email"], "password": "wrong_" + user_data["password"]}
        response = requests.post(LOGIN_URL, json=payload)
        assert response.status_code == 401 
        assert response.json()["success"] == False
        assert "email or password" in response.json()["message"].lower(), (
            f"Ожидалась ошибка 401, получен статус {response.status_code}, тело: {response.text}"
        )
