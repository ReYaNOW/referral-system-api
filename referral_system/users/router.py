from fastapi import APIRouter, status

from referral_system.auth.dependencies import AnnCurrentUser
from referral_system.users import schemas
from referral_system.users.dependencies import AnnQueryRequest, AnnUserService

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/me', response_model=schemas.UserRead)
async def show_logged_user(user: AnnCurrentUser):
    return user


@router.post('', response_model=schemas.UserRead)
async def create_user(new_user: schemas.UserCreate, service: AnnUserService):
    user = await service.create_user(new_user)
    return user


@router.get('/{id}', response_model=schemas.UserRead)
async def read_user(id: int, service: AnnUserService):
    user = await service.find_user(id)
    return user


@router.get('', response_model=schemas.UserListResponse)
async def list_users(query: AnnQueryRequest, service: AnnUserService):
    paginated_users = await service.paginate_users(query)
    return paginated_users


@router.get('/{id}/referrals', response_model=schemas.UserListResponse)
async def list_referrals(
    id: int, query: AnnQueryRequest, service: AnnUserService
):
    paginated_users = await service.paginate_users(query, referred_by_id=id)
    return paginated_users


@router.patch(
    '/{id}',
    response_model=schemas.UserRead,
    summary='Update certain fields of existing user',
)
async def update_user(
    id: int,
    user: AnnCurrentUser,
    new_values: schemas.UserUpdate,
    service: AnnUserService,
):
    updated_user = await service.update_user(user, id, new_values)
    return updated_user


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, user: AnnCurrentUser, service: AnnUserService):
    await service.delete_user(user, id)
