from typing import Annotated

from fastapi import Depends

from referral_system.referrals.service import ReferralService

AnnReferralService = Annotated[ReferralService, Depends(ReferralService)]
