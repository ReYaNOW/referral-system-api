import asyncio

import redis.asyncio as redis

from referral_system.config import config
from referral_system.referrals.models import ReferralCode
from referral_system.referrals.schemas import ReferralCodeRead


class RedisService:
    def __init__(self):
        self.redis_client = redis.from_url(
            config.redis_url.unicode_string(),
            decode_responses=True,
        )
        self.ttl = config.redis_ttl

    async def set(self, key: str, value: str) -> None:
        await self.redis_client.setex(key, self.ttl, value)

    async def get(self, key: str) -> str | None:
        return await self.redis_client.get(key)

    async def delete(self, key: str) -> None:
        await self.redis_client.delete(key)

    async def cache_referral_code(self, key: str, code: ReferralCode) -> None:
        code_dict = ReferralCodeRead.model_validate(code).model_dump_json()
        await self.set(key, code_dict)

    async def cache_code_by_multiple_fields(
        self, *fields: str, code: ReferralCode
    ) -> None:
        tasks = [self.cache_referral_code(field, code) for field in fields]
        await asyncio.gather(*tasks)

    async def delete_code_by_multiple_fields(self, *fields: str) -> None:
        tasks = [self.delete(field) for field in fields]
        await asyncio.gather(*tasks)
