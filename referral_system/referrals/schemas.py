from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic.json_schema import SkipJsonSchema


class ReferralCodeCreate(BaseModel):
    expiration: datetime

    code: SkipJsonSchema[str | None] = None
    user_id: SkipJsonSchema[int | None] = None


class ReferralCodeRead(BaseModel):
    id: int
    code: str
    expiration: datetime
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class ReferralCodeUpdate(BaseModel):
    expiration: datetime | None = None
