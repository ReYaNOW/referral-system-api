from fastapi import APIRouter

from referral_system.auth.dependencies import AnnAuthService, AnnFormData
from referral_system.auth.schemas import AccessToken

router = APIRouter(prefix='', tags=['Token'])


@router.post('/token', response_model=AccessToken)
async def receive_token(form_data: AnnFormData, service: AnnAuthService):
    token = await service.create_token(form_data.username, form_data.password)
    return AccessToken(access_token=token)
