from pydantic import EmailStr
from sqlalchemy import delete, insert, update
from sqlalchemy.future import select

from referral_system.referrals.models import ReferralCode
from referral_system.referrals.schemas import (
    ReferralCodeCreate,
    ReferralCodeUpdate,
)
from referral_system.users.models import User
from referral_system.utils.repository import SQLAlchemyRepository
from referral_system.utils.types import ResultType


class ReferralRepository(SQLAlchemyRepository[ReferralCode]):
    table_verbose_name = 'referral code'

    async def create_referral_code(
        self, code_create: ReferralCodeCreate
    ) -> ReferralCode:
        stmt = (
            insert(ReferralCode)
            .values(code_create.model_dump())
            .returning(ReferralCode)
        )
        return await self.execute(stmt, commit=True)

    async def find_referral_code_by_user_id(
        self, user_id: int
    ) -> ReferralCode:
        query = select(ReferralCode).where(ReferralCode.user_id == user_id)
        return await self.execute(query)

    async def find_referral_code_by_email(
        self, email: EmailStr
    ) -> ReferralCode:
        query = (
            select(ReferralCode)
            .join(ReferralCode.owner)
            .where(User.email == email)
        )

        return await self.execute(query)

    async def find_referral_code_by_code(
        self, code: str
    ) -> ReferralCode | None:
        query = select(ReferralCode).where(ReferralCode.code == code)
        return await self.execute(query, raise_on_none=False)

    async def update_expiration_of_code_by_user_id(
        self,
        user_id: int,
        new_values: ReferralCodeUpdate,
    ) -> ReferralCode:
        stmt = (
            update(ReferralCode)
            .values(new_values.model_dump())
            .where(ReferralCode.user_id == user_id)
            .returning(ReferralCode)
        )
        return await self.execute(stmt, commit=True)

    async def delete_referral_code_by_user_id(
        self, user_id: int
    ) -> ReferralCode:
        stmt = (
            delete(ReferralCode)
            .where(ReferralCode.user_id == user_id)
            .returning(ReferralCode)
        )
        return await self.execute(stmt, ResultType.ONE, commit=True)
