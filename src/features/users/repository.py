from sqlalchemy import func, select
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.base_repository import BaseRepository
from src.core.security import get_password_hash
from src.features.users.models import User
from src.features.users.schemas import UserUpdate, UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def update(self, user_id: int, user_in: UserUpdate) -> User:
        user = await self.session.get(User, user_id)
        if not user:
            raise ValueError("User not found")

        for key, value in user_in.model_dump(exclude_unset=True).items():
            setattr(user, key, value)

        return user

    async def create(self, obj_in: UserCreate) -> User:
        # Преобразуем схему в словарь, удаляем пароль
        user_data = obj_in.model_dump(exclude={"password"})

        # Хешируем пароль и добавляем в данные
        hashed_password = get_password_hash(obj_in.password)
        user = User(**user_data, hashed_password=hashed_password)

        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def update_password(self, user_id: int, hashed_password: str) -> User:
        user = await self.session.get(User, user_id)
        if not user:
            raise ValueError("User not found")

        user.hashed_password = hashed_password
        self.session.add(user)
        return user
