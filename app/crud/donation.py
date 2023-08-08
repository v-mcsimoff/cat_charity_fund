from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def get_donations_by_charityproject(
            self,
            *,
            charityproject_id: int,
            donation_id: Optional[int] = None,
            session: AsyncSession,
    ) -> list[Donation]:
        select_stmt = select(Donation).where(
            Donation.charityproject_id == charityproject_id,
        )
        if donation_id is not None:
            select_stmt = select_stmt.where(
                Donation.id != donation_id
            )
        donations = await session.execute(select_stmt)
        donations = donations.scalars().all()
        return donations

    async def get_by_user(
            self,
            user: User,
            session: AsyncSession
    ):
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
