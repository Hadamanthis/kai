

from user.models import User
from user.repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def save(self, user: User) -> User | None:
        existing_user = self.user_repository.get_by_username(user.username)
        if existing_user is not None:
            return None
        
        return self.user_repository.save(user)


    def get_by_username(self, username: str) -> User:
        return self.user_repository.get_by_username(username)