import pytest
from helpers import register_new_user, delete_user

@pytest.fixture
def auth_token():
    """Создаёт нового пользователя, возвращает токен, удаляет после теста."""
    email, password, name, token = register_new_user()
    yield token
    if token:
        delete_user(token)

