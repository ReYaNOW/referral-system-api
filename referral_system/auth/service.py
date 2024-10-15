from datetime import UTC, datetime, timedelta

import jwt

from referral_system.auth.exceptions import (
    credentials_exception,
    expired_token_exception,
    invalid_credentials,
    not_found_exception,
)
from referral_system.auth.utills import AnnPasswordService
from referral_system.config import config
from referral_system.users.dependencies import AnnUserService
from referral_system.users.models import User


class AuthService:
    secret_key = config.secret_key
    access_token_expire_minutes = config.access_token_expire_minutes
    algorithm = 'HS256'

    def __init__(
        self,
        user_service: AnnUserService,
        password_service: AnnPasswordService,
    ):
        self.user_service = user_service
        self.password_service = password_service

    def generate_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        to_encode = data.copy()
        expire = datetime.now(tz=UTC) + (
            expires_delta
            if expires_delta
            else timedelta(minutes=self.access_token_expire_minutes)
        )
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(
            to_encode, self.secret_key, algorithm=self.algorithm
        )
        return encoded_jwt

    async def create_token(self, username: str, password: str) -> str:
        user = await self.user_service.find_user_by_username(username)

        if not user:
            raise invalid_credentials

        if not await self.password_service.a_verify_pass(
            password, user.hashed_password
        ):
            raise invalid_credentials

        token_data = {'sub': user.id}

        access_token = self.generate_access_token(data=token_data)

        return access_token

    def decode_access_token(self, token: str) -> int:
        try:
            payload = jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm]
            )

            user_id: str = payload.get('sub')
            if user_id is None:
                raise credentials_exception

            return int(user_id)

        except jwt.ExpiredSignatureError:
            raise expired_token_exception from None

        except jwt.PyJWTError:
            raise credentials_exception from None

    async def find_user_by_token(self, token: str) -> User:
        id_ = self.decode_access_token(token)

        user = await self.user_service.find_user(id_)
        if user is None:
            raise not_found_exception

        return user
