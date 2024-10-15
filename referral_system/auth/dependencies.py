from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from referral_system.auth.service import AuthService
from referral_system.users.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
AnnOauth2Scheme = Annotated[str, Depends(oauth2_scheme)]

AnnFormData = Annotated[OAuth2PasswordRequestForm, Depends()]

AnnAuthService = Annotated[AuthService, Depends(AuthService)]


async def get_current_user(
    token: AnnOauth2Scheme, auth_service: AnnAuthService
) -> User:
    user = await auth_service.find_user_by_token(token)
    return user


AnnCurrentUser = Annotated[User, Depends(get_current_user)]
