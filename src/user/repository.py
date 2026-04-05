from sqlalchemy import select
from user.models import User
from sqlalchemy.orm import Session


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, new_user: User) -> User:
        self.db.add(new_user)
        self.db.commit()

        self.db.refresh(new_user)

        return new_user

    def get_by_username(self, username: str) -> User | None:
        existing_user = self.db.execute(
            select(User)
            .where(User.username == username)
            .limit(1)
        ).scalars().one_or_none()

        return existing_user