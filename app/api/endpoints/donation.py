from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.crud.charity_project import charity_project_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB
from app.services.investment import charges


router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude={
        'user_id', 'fully_invested',
        'invested_amount', 'close_date'}
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(
        donation, session, user
    )
    await charges(
        undivided=new_donation,
        crud_class=charity_project_crud,
        session=session
    )
    return new_donation


@router.get(
    '/',
    response_model=List[DonationDB],
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def get_all_donations(session: AsyncSession = Depends(get_async_session)):
    """For superusers only."""
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude={
        'user_id', 'fully_invested',
        'invested_amount', 'close_date'},
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Gets a list of all donations for the current user."""
    donations = await donation_crud.get_by_user(
        session=session, user=user
    )
    return donations


@router.delete('/{donation_id}', deprecated=True)
def delete_donation(donation_id: int):
    raise HTTPException(
        status_code=404,
        detail='Deletion of donations is forbidden!'
    )


@router.patch('/{donation_id}', deprecated=True)
def update_donation(donation_id: int):
    raise HTTPException(
        status_code=404,
        detail='Changing donations is forbidden!'
    )
