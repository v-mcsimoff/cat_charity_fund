from datetime import datetime 

from sqlalchemy.ext.asyncio import AsyncSession 

from app.core.db import Base 
from app.models.charity_project import CharityProject
from app.models.donation import Donation

async def entry_to_db(object: Base, session: AsyncSession) -> Base:
    if isinstance(object, (CharityProject, Donation)):
        await session.commit()
        await session.refresh(object)
        return object
    else:
        raise ValueError('Тип объекта не поддерживается') 

def close_object(object: Base) -> None: 
    if isinstance(object, CharityProject):
        object.fully_invested = (object.full_amount == object.invested_amount) 
        if object.fully_invested: 
            object.close_date = datetime.now() 

async def charges( 
    undivided: CharityProject, 
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
