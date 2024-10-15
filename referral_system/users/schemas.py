from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    computed_field,
)
from pydantic.json_schema import SkipJsonSchema


class UserCreate(BaseModel):
    username: str = Field(examples=['Username'], max_length=50)
    email: EmailStr = Field(examples=['developer@gmail.com'], max_length=255)
    password: str = Field(
        exclude=True, examples=['super_secret_password'], max_length=255
    )
    referral_code: str | None = Field(
        default=None, exclude=True, examples=[''], max_length=255
    )

    hashed_password: SkipJsonSchema[str | None] = None
    referred_by_id: SkipJsonSchema[int | None] = None


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: str | None = Field(
        default=None, examples=['Username'], max_length=50
    )
    email: EmailStr | None = Field(
        default=None, examples=['developer@gmail.com'], max_length=255
    )
    password: str | None = Field(
        default=None, exclude=True, examples=['secret_pass'], max_length=255
    )

    hashed_password: SkipJsonSchema[str | None] = None


AvailableOrderBy = Literal['id', 'username']


class UserListRequest(BaseModel):
    page: int = 1
    limit: int = 10
    order_by: AvailableOrderBy = 'id'


class CreateResponse(BaseModel):
    user_id: int


class UserListResponse(BaseModel):
    data: list[UserRead]
    total: int
    current: int

    @computed_field
    @property
    def previous(self) -> int | None:
        return self.current - 1 if self.current > 1 else None

    @computed_field
    @property
    def next(self) -> int | None:
        return self.current + 1 if self.current != self.total else None
