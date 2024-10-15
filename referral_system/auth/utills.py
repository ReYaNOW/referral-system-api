from typing import Annotated

from fastapi import Depends
from passlib.context import CryptContext
from starlette.concurrency import run_in_threadpool


class PasswordService:
    pwd_context = CryptContext(
        schemes=['argon2'],
        argon2__memory_cost=4096,
        argon2__parallelism=2,
        deprecated='auto',
    )

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)

    def _get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def a_verify_pass(self, password: str, hashed_password: str) -> bool:
        return await run_in_threadpool(
            self._verify_password, password, hashed_password
        )

    async def a_get_password_hash(self, password: str) -> str:
        return await run_in_threadpool(self._get_password_hash, password)


AnnPasswordService = Annotated[PasswordService, Depends(PasswordService)]
