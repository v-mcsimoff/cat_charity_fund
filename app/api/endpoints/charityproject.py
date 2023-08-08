from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charityproject import charityproject_crud
from app.schemas.charityproject import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.crud.donation import donation_crud
from app.api.validators import (
    check_name_duplicate, check_charityproject_exists,
    check_fully_invested, check_charityproject_before_edit,
    check_invested_amount_is_null)
from app.core.user import current_superuser
from app.services.investment import charges

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charityproject(
        charityproject: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(charityproject.name, session)
    new_charityproject = await charityproject_crud.create(charityproject, session)
    await charges(
        undivided=new_charityproject,
        crud_class=donation_crud,
        session=session
    )
    return new_charityproject


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charityprojects(session: AsyncSession = Depends(get_async_session)):
    all_charityprojects = await charityproject_crud.get_multi(session)
    return all_charityprojects


@router.patch(
    '/{charityproject_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charityproject(
        charityproject_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charityproject = await check_charityproject_exists(
        charityproject_id, session
    )
    await check_fully_invested(
        charityproject_id, session
    )
    if obj_in.full_amount:
        charityproject = check_charityproject_before_edit(
            charityproject_id, obj_in.full_amount, session
        )
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)

    charityproject = await charityproject_crud.update(
        charityproject, obj_in, session
    )
    return charityproject


@router.delete(
    '/{charityproject_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charityproject(
        charityproject_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charityproject = await check_charityproject_exists(
        charityproject_id, session
    )
    await check_invested_amount_is_null(
        charityproject_id, session
    )
    await check_fully_invested(charityproject_id, session)
    charityproject = await charityproject_crud.remove(
        charityproject, session
    )
    return charityproject
