from typing import Annotated

from fastapi import Depends

from referral_system.users.schemas import UserListRequest
from referral_system.users.service import UserService

AnnUserService = Annotated[UserService, Depends(UserService)]
AnnQueryRequest = Annotated[UserListRequest, Depends()]
