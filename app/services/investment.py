from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base


async def entry_to_db(object: Base, session: AsyncSession) -> Base:
    await session.commit()
    await session.refresh(object)
    return object


def close_object(object: Base) -> None:
    object.fully_invested = (object.full_amount == object.invested_amount)
    if object.fully_invested:
        object.close_date = datetime.now()


async def charges(
    undivided: Base,
    crud_class: Base,
    session: AsyncSession
) -> None:
    receptions = await crud_class.get_opened_objects(
        session=session
    )
    for reception in receptions:
        needed = undivided.full_amount - undivided.invested_amount
        if not needed:
            break
        available = reception.full_amount - reception.invested_amount
        to_add = min(needed, available)
        reception.invested_amount += to_add
        undivided.invested_amount += to_add
        close_object(reception)

    close_object(undivided)

    await entry_to_db(
        object=undivided,
        session=session
    )
