from sqlalchemy import ScalarResult, delete, func, insert, update
from sqlalchemy.future import select

from referral_system.users.models import User
from referral_system.users.schemas import (
    AvailableOrderBy,
    UserCreate,
    UserUpdate,
)
from referral_system.utils.repository import SQLAlchemyRepository
from referral_system.utils.types import ResultType


class UserRepository(SQLAlchemyRepository[User]):
    table_verbose_name = 'User'

    async def create_user(self, user_create: UserCreate) -> User:
        stmt = insert(User).values(user_create.model_dump()).returning(User)
        return await self.execute(stmt, commit=True)

    async def find_user(self, user_id: int) -> User:
        query = select(User).filter(User.id == user_id)
        return await self.execute(query)

    async def find_user_by_username(self, username: str) -> User | None:
        query = select(User).where(User.username == username)
        return await self.execute(query, raise_on_none=False)

    async def find_users(
        self,
        page: int,
        limit: int,
        order_by: AvailableOrderBy,
        referred_by_id: int,
    ) -> ScalarResult[User]:
        offset_value = page * limit - limit

        query = (
            select(User).offset(offset_value).limit(limit).order_by(order_by)
        )

        if referred_by_id:
            query = query.where(User.referred_by_id == referred_by_id)

        return await self.execute(query, ResultType.MANY)

    async def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        stmt = (
            update(User)
            .values(user_update.model_dump(exclude_none=True))
            .where(User.id == user_id)
            .returning(User)
        )
        return await self.execute(stmt, commit=True)

    async def delete_user(self, user_id: int) -> None:
        stmt = delete(User).where(User.id == user_id)
        await self.execute(stmt, commit=True)

    async def count_records(self) -> int:
        query = select(func.count()).select_from(User)
        return await self.execute(query)
