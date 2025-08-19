import bcrypt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import get_password_hash
from src.features.users.models import User
from .schemas import UserRead, UserUpdate, UserCreate
from src.features.users.repository import UserRepository
from src.shared.uow import UnitOfWork

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)

    async def get_all(self) -> list[UserRead]:
        users = await self.repo.get_all()
        return [UserRead.model_validate(user) for user in users]

    async def get_by_id(self, user_id: int) -> UserRead:
        user_out = await self.repo.get_by_id(user_id)
        return UserRead.model_validate(user_out)

    async def get_by_username(self, username: str) -> UserRead:
        user_out = await self.repo.get_by_username(username)
        return UserRead.model_validate(user_out)

    async def get_by_email(self, user_email: str) -> UserRead:
        user_out = await self.repo.get_by_email(user_email)
        return UserRead.model_validate(user_out)

    async def update_user(self, user_id: int, user_in: UserUpdate) -> UserRead:
        user_out = await self.repo.update(user_id, user_in)
        return UserRead.model_validate(user_out)

    async def delete_user(self, user_id: int):
        return await self.repo.delete(user_id)

    async def create_user(self, user_in: UserCreate) -> UserRead:

        user_data = user_in.model_dump(exclude={"password"})

        hashed_password = get_password_hash(user_in.password)
        user = User(**user_data, hashed_password=hashed_password)

        user_out = await self.repo.create(user_in)
        return UserRead.model_validate(user_out)

    async def is_repeat(self, username: str, email: str) -> bool:
        check_name = await self.repo.get_by_username(username)
        check_email = await self.repo.get_by_email(email)
        if check_name or check_email:
            return True
        return False


class PasswordService:
    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
