import logging
from datetime import datetime

import httpx
from fastapi import status
from pydantic import EmailStr

from referral_system.auth.utills import AnnPasswordService
from referral_system.config import config
from referral_system.database import AnnAsyncSession
from referral_system.referrals.dependencies import AnnReferralService
from referral_system.users.exception import (
    expired_referral_code_exc,
    insufficient_permissions_exc,
    invalid_email_exc,
    invalid_referral_code_exc,
)
from referral_system.users.models import User
from referral_system.users.repository import UserRepository
from referral_system.users.schemas import (
    UserCreate,
    UserListRequest,
    UserListResponse,
    UserUpdate,
)

logging.basicConfig(
    format='Email validation failed for %(email)s. '
    'Status code: %(status_code)s, '
    'Response: %(message)s',
    level=logging.ERROR,
)


url = 'https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}'
URL_TEMPLATE = url.replace('{api_key}', config.hunterio_api_key)


class UserService:
    def __init__(
        self,
        session: AnnAsyncSession,
        password_service: AnnPasswordService,
        referral_code_service: AnnReferralService,
    ):
        self.user_repo = UserRepository(session)
        self.password_service = password_service
        self.referral_service = referral_code_service

    async def create_user(self, new_user: UserCreate) -> User:
        if not await self.validate_email(new_user.email):
            raise invalid_email_exc

        hashed_password = await self.password_service.a_get_password_hash(
            new_user.password
        )
        new_user.hashed_password = hashed_password

        if new_user.referral_code:
            referral = await self.referral_service.find_referral_code_by_code(
                new_user.referral_code
            )

            if not referral:
                raise invalid_referral_code_exc

            if referral.expiration < datetime.now(
                tz=referral.expiration.tzinfo
            ):
                raise expired_referral_code_exc

            new_user.referred_by_id = referral.user_id

        created_user = await self.user_repo.create_user(new_user)
        return created_user

    async def find_user(self, user_id: int) -> User:
        return await self.user_repo.find_user(user_id)

    async def find_user_by_username(self, username: str) -> User | None:
        return await self.user_repo.find_user_by_username(username)

    async def paginate_users(
        self, query: UserListRequest, referred_by_id: int | None = None
    ) -> UserListResponse:
        users = await self.user_repo.find_users(
            query.page, query.limit, query.order_by, referred_by_id
        )
        total_records = await self.user_repo.count_records()
        pages = (total_records + query.limit - 1) // query.limit
        return UserListResponse(data=users, total=pages, current=query.page)

    async def update_user(
        self, curr_user: User, user_id: int, user_update: UserUpdate
    ) -> User:
        if curr_user.id != user_id:
            raise insufficient_permissions_exc

        if user_update.password:
            user_update.hashed_password = (
                await self.password_service.a_get_password_hash(
                    user_update.password
                )
            )

        updated_user = await self.user_repo.update_user(
            user_id=user_id, user_update=user_update
        )
        return updated_user

    async def delete_user(self, curr_user: User, user_id: int) -> None:
        if curr_user.id != user_id:
            raise insufficient_permissions_exc

        await self.user_repo.delete_user(user_id)

    async def validate_email(self, email: EmailStr) -> bool:
        if not config.hunterio_api_key:
            return True

        async with httpx.AsyncClient() as client:
            response = await client.get(
                URL_TEMPLATE.format(email=email), timeout=10
            )

            if response.status_code == status.HTTP_200_OK:
                resp_dict: dict = response.json()
                data = resp_dict.get('data')

                if isinstance(data, dict):
                    return data.get('status') == 'valid'
                return False
            logging.error(
                response.text,
                extra={'email': email, 'status_code': response.status_code},
            )
            return False
