from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt
from sqlalchemy.orm import validates


class DonationBase(BaseModel):
    full_amount: Optional[PositiveInt]
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    full_amount: PositiveInt


class DonationDB(DonationBase):
    id: int
    user_id: Optional[int]
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    @validates("full_amount")
    def validate_full_amount(self, key, full_amount):
        if full_amount < self.invested_amount:
            raise ValueError("Unable to set an amount less than the amount previously invested")
        return full_amount

    class Config:
        orm_mode = True
