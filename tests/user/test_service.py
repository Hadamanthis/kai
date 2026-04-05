from user.models import User
from unittest.mock import MagicMock
from user.repository import UserRepository
from user.service import UserService


def test_user_save_sucess():
    new_user = User(username="usuario_teste", name="Teste")

    user_repository = MagicMock()
    user_repository.save.return_value = new_user
    user_repository.get_by_username.return_value = None

    user_service = UserService(user_repository)
    user = user_service.save(new_user)

    user_repository.get_by_username.assert_called_once_with(new_user.username)
    user_repository.save.assert_called_once_with(new_user)
    assert user is not None
    

def test_user_save_fail_username_already_exists():
    new_user = User(username="usuario_teste", name="Teste")

    user_repository = MagicMock()
    user_repository.save.return_value = None
    user_repository.get_by_username.return_value = new_user

    user_service = UserService(user_repository)

    user = user_service.save(new_user)

    user_repository.get_by_username.assert_called_once_with(new_user.username)
    user_repository.save.assert_not_called()
    assert user is None

def test_user_get_by_username_sucess():
    new_user = User(username="usuario_teste", name="Teste")

    user_repository = MagicMock()
    user_repository.get_by_username.return_value = new_user

    user_service = UserService(user_repository)

    user = user_service.get_by_username("usuario_teste")

    user_repository.get_by_username.assert_called_once_with("usuario_teste")
    assert user is not None

def test_user_get_by_username_fail_inexistent_username():
    new_user = User(username="usuario_teste", name="Teste")

    user_repository = MagicMock()
    user_repository.get_by_username.return_value = None

    user_service = UserService(user_repository)

    user = user_service.get_by_username("username_inexistente")

    user_repository.get_by_username.assert_called_with("username_inexistente")
    assert user is None