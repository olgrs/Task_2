import pytest
from api.user_api import UserApi

from helpers import generate_random_string


@pytest.fixture
def new_user(user_data):
    response = UserApi.create_user(user_data)
    yield response, user_data
    if response.status_code == 200:
        token = response.json()["accessToken"]
        UserApi.delete_user(token)

@pytest.fixture
def user_data():
    email = f"test_{generate_random_string()}@example.com"
    password = generate_random_string()
    name = f"User_{generate_random_string()}"
    user_data = {"email": email, "password": password, "name": name}
    return user_data
