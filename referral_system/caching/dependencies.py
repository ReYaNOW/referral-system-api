from typing import Annotated

from fastapi import Depends

from referral_system.caching.service import RedisService

AnnRedisService = Annotated[RedisService, Depends(RedisService)]
