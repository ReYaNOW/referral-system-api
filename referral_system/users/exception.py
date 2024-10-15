from fastapi import HTTPException, status

invalid_referral_code_exc = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail='Referral code is invalid',
)

expired_referral_code_exc = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail='Referral code has expired'
)

invalid_email_exc = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail="Email address is not real or we wasn't able to validate it",
)

insufficient_permissions_exc = HTTPException(
    status_code=403, detail='Insufficient permissions'
)


class CodeExistsExc(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(
            status_code=409,
            detail=f'referral code with user_id={user_id} already exists',
        )
