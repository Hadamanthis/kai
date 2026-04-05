from user.models import User
from sqlalchemy.orm import Session
from user.repository import UserRepository

def test_user_save_sucess(db: Session):
    user_repository = UserRepository(db)

    user_repository.save(User(username="usuario_teste", name="Teste"))

    user = user_repository.get_by_username("usuario_teste")

    assert user is not None
    assert user.name == "Teste"

def test_user_get_by_username_sucess(db: Session):
    user_repository = UserRepository(db)

    user_repository.save(User(username="usuario_teste", name="Teste"))

    user = user_repository.get_by_username("usuario_teste")

    assert user is not None
    assert user.name == "Teste"

def test_user_get_by_username_fail(db: Session):
    user_repository = UserRepository(db)

    user_repository.save(User(username="usuario_teste", name="Teste"))

    user = user_repository.get_by_username("username_inexistente")

    assert user is None