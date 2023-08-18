from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicate(
        charity_project_name: str,
        session: AsyncSession,
) -> None:
    charity_project_id = await charity_project_crud.get_charity_project_id_by_name(
        charity_project_name, session
    )
    if charity_project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return charity_project


async def check_charity_project_before_edit(
    charity_project: CharityProject,
    obj_in: CharityProjectUpdate
) -> CharityProject:
    if charity_project.invested_amount > obj_in.full_amount:
        raise HTTPException(
            status_code=422,
            detail='Внесённая сумма должна быть больше новой!')
    if charity_project.invested_amount == obj_in.full_amount:
        charity_project.fully_invested = True
        charity_project.close_date = datetime.datetime.now()
    return charity_project


async def check_invested_amount_is_null(
        charity_project_id: int,
        session: AsyncSession
):
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project.invested_amount != 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_fully_invested(charity_project_id: int, session: AsyncSession) -> None:
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )
