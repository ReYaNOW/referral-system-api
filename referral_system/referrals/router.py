from fastapi import APIRouter, status
from pydantic import EmailStr

from referral_system.auth.dependencies import AnnCurrentUser
from referral_system.referrals import schemas
from referral_system.referrals.dependencies import AnnReferralService

router = APIRouter(prefix='/referral_code', tags=['ReferralCode'])


@router.post('', response_model=schemas.ReferralCodeRead)
async def create_code(
    user: AnnCurrentUser,
    new_code: schemas.ReferralCodeCreate,
    service: AnnReferralService,
):
    referral_code = await service.create_referral_code(user, new_code)
    return referral_code


@router.get('', response_model=schemas.ReferralCodeRead)
async def read_code(user: AnnCurrentUser, service: AnnReferralService):
    referral_code = await service.find_referral_code_by_user(user)
    return referral_code


@router.get('/find_by_email', response_model=schemas.ReferralCodeRead)
async def read_code_by_email(email: EmailStr, service: AnnReferralService):
    referral_code = await service.find_referral_code_by_email(email)
    return referral_code


@router.patch(
    '',
    response_model=schemas.ReferralCodeRead,
    summary="Update expiration datetime of user's referral code",
)
async def update_code(
    user: AnnCurrentUser,
    new_values: schemas.ReferralCodeUpdate,
    service: AnnReferralService,
):
    updated_code = await service.update_expiration_of_code(user, new_values)
    return updated_code


@router.delete('', status_code=status.HTTP_204_NO_CONTENT)
async def delete_code(user: AnnCurrentUser, service: AnnReferralService):
    await service.delete_referral_code(user)
