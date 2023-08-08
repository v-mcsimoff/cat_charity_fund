from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charityproject_crud
from app.models import CharityProject


async def check_name_duplicate(
        charityproject_name: str,
        session: AsyncSession,
) -> None:
    charityproject_id = await charityproject_crud.get_charityproject_id_by_name(
        charityproject_name, session
    )
    if charityproject_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким названием уже существует!',
        )

        
async def check_charityproject_exists(
        charityproject_id: int,
        session: AsyncSession,
) -> CharityProject:
    charityproject = await charityproject_crud.get(charityproject_id, session)
    if charityproject is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return charityproject


async def check_charityproject_before_edit(
        charityproject_id: int,
        full_amount: int,
        session: AsyncSession,
):
    charityproject = await charityproject_crud.get(
        obj_id=charityproject_id, session=session,
    )
    if charityproject.invested_amount:
        if charityproject.invested_amount > full_amount:
            raise HTTPException(
                status_code=400,
                detail='Внесённая сумма должна быть больше новой!'
            )
        if charityproject.invested_amount == full_amount:
            charityproject.fully_invested = True
    return charityproject


async def check_invested_amount_is_null(
        charityproject_id: int,
        session: AsyncSession
):
    charityproject = await charityproject_crud.get(charityproject_id, session)
    if charityproject.invested_amount != 0:
        raise HTTPException(
            status_code=400,
            detail='Невозможно удалить проект с внесёнными пожертвованиями'
        )


async def check_fully_invested(charityproject_id: int, session: AsyncSession):
    charityproject = await charityproject_crud.get(charityproject_id, session)
    if charityproject.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Невозможно изменить или удалить закрытый проект'
        )
