from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from referral_system.database import Base

if TYPE_CHECKING:
    from referral_system.users.models import User

metadata = Base.metadata


class ReferralCode(Base):
    __tablename__ = 'referral_codes'

    code: Mapped[str] = mapped_column(unique=True, index=True)
    expiration: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), unique=True, index=True
    )

    owner: Mapped['User'] = relationship(
        'User',
        back_populates='referral_code',
        uselist=False,
    )
