from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from referral_system.database import Base

if TYPE_CHECKING:
    from referral_system.referrals.models import ReferralCode


metadata = Base.metadata


class User(Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    referred_by_id: Mapped[int | None] = mapped_column(
        ForeignKey('users.id'), nullable=True, index=True
    )

    referral_code: Mapped['ReferralCode'] = relationship(
        'ReferralCode',
        back_populates='owner',
        uselist=False,
    )
