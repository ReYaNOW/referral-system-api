from datetime import datetime

from pydantic import EmailStr

from referral_system.caching.dependencies import AnnRedisService
from referral_system.database import AnnAsyncSession
from referral_system.referrals.models import ReferralCode
from referral_system.referrals.repository import ReferralRepository
from referral_system.referrals.schemas import (
    ReferralCodeCreate,
    ReferralCodeRead,
    ReferralCodeUpdate,
)
from referral_system.users.exception import CodeExistsExc
from referral_system.users.models import User


class ReferralService:
    def __init__(
        self, session: AnnAsyncSession, redis_service: AnnRedisService
    ):
        self.referral_repo = ReferralRepository(session)
        self.redis_service = redis_service

    async def create_referral_code(
        self, user: User, code_create: ReferralCodeCreate
    ) -> ReferralCode:
        code_in_db = await user.awaitable_attrs.referral_code
        if code_in_db:
            # For a prettier error message instead of the one from
            # error handler
            raise CodeExistsExc(user.id)

        code = self.generate_referral_code(
            user.username, code_create.expiration
        )
        code_create.code = code
        code_create.user_id = user.id

        new_referral_code = await self.referral_repo.create_referral_code(
            code_create
        )
        return new_referral_code

    async def find_referral_code_by_user(self, user: User) -> ReferralCode:
        return await self.referral_repo.find_referral_code_by_user_id(user.id)

    async def find_referral_code_by_email(
        self, email: EmailStr
    ) -> ReferralCode | ReferralCodeRead:
        code_from_cache = await self.redis_service.get(email)
        if code_from_cache:
            return ReferralCodeRead.model_validate_json(code_from_cache)

        code = await self.referral_repo.find_referral_code_by_email(email)
        await self.redis_service.cache_referral_code(email, code)
        return code

    async def find_referral_code_by_code(
        self, code: str
    ) -> ReferralCode | ReferralCodeRead:
        code_from_cache = await self.redis_service.get(code)
        if code_from_cache:
            return ReferralCodeRead.model_validate_json(code_from_cache)

        code_obj = await self.referral_repo.find_referral_code_by_code(code)
        if code_obj:
            await self.redis_service.cache_referral_code(code, code_obj)
        return code_obj

    async def update_expiration_of_code(
        self,
        user: User,
        new_values: ReferralCodeUpdate,
    ) -> ReferralCode:
        updated_code = (
            await self.referral_repo.update_expiration_of_code_by_user_id(
                user.id, new_values
            )
        )

        await self.redis_service.cache_code_by_multiple_fields(
            user.email, updated_code.code, code=updated_code
        )

        return updated_code

    async def delete_referral_code(self, user: User) -> None:
        deleted_code = (
            await self.referral_repo.delete_referral_code_by_user_id(user.id)
        )
        await self.redis_service.delete_code_by_multiple_fields(
            user.email, deleted_code.code
        )

    def generate_referral_code(
        self, username: str, expiration: datetime
    ) -> str:
        return f'{username}{expiration.__hash__()}'
