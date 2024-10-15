from fastapi import FastAPI

from referral_system.auth.router import router as auth_router
from referral_system.referrals.router import router as referrals_router
from referral_system.users.router import router as users_router

tags_metadata = [
    {
        'name': 'Token',
        'description': 'Receive **access token** by credentials',
    },
    {
        'name': 'Users',
        'description': 'Operations with **users**.',
    },
    {
        'name': 'ReferralCode',
        'description': 'Operations with **referral code** for '
        'current logged in user',
    },
]

app = FastAPI(
    title='Referral System',
    openapi_tags=tags_metadata,
    swagger_ui_parameters={
        'persistAuthorization': True,
        'defaultModelsExpandDepth': 0,
    },
)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(referrals_router)
