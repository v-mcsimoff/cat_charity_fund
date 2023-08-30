from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
        charity_project_name: str,
        session: AsyncSession,
) -> None:
    """Project name validation"""
    charity_project_id = await charity_project_crud.get_charity_project_id_by_name(
        charity_project_name, session
    )
    if charity_project_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='A project with this name already exists!',
        )


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Project existence validation"""
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Project not found!'
        )
    return charity_project


async def check_charity_project_before_edit(
        charity_project_id: int,
        full_amount: int,
        session: AsyncSession) -> CharityProject:
    """Donation amount validation"""
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if full_amount is not None:
        if charity_project.invested_amount > full_amount:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='The invested amount must be greater than the new amount!'
            )
        if charity_project.invested_amount == full_amount:
            charity_project.fully_invested = True
        return charity_project


async def check_invested_amount_is_null(
        charity_project_id: int,
        session: AsyncSession
):
    """Invested amount check"""
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project.invested_amount != 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The project has been contributed to, cannot be deleted!'
        )


async def check_fully_invested(charity_project_id: int, session: AsyncSession) -> None:
    """Fully invested project check"""
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='A closed project cannot be edited!'
        )
