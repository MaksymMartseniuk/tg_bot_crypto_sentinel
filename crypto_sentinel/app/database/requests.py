from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from app.database.models import User, Alerts

async def set_user(session: AsyncSession, tg_id: int, username: str | None):
    stmt = insert(User).values(
        tg_id=tg_id, 
        username=username
    ).on_conflict_do_update(
        index_elements=['tg_id'],
        set_={'username': username}
    )
    await session.execute(stmt)
    await session.commit()

async def add_alert(session: AsyncSession, tg_id: int, symbol: str, target_price: float, direction: str):
        user=await session.scalar(select(User).where(User.tg_id==tg_id))
        if user:
            alert=Alerts(user_id=user.tg_id,
                         symbol=symbol.upper(),
                         target_price=target_price,
                         direction=direction)
            session.add(alert)
            await session.commit()
            return True
        return False
    
async def get_user_alerts(session: AsyncSession, tg_id: int):
    result = await session.scalars(
        select(Alerts).where(Alerts.user_id == tg_id)
    )
    return result.all()
    
async def get_active_alerts(session: AsyncSession):
    result = await session.scalars(
        select(Alerts)
        .options(joinedload(Alerts.user))
        .where(Alerts.is_active == True)
    )

async def set_user_language(session: AsyncSession, tg_id: int, lang_code: str):
    await session.execute(
        update(User)
        .where(User.tg_id == tg_id)
        .values(language=lang_code)
    )
    await session.commit()

async def get_user(session: AsyncSession, tg_id: int):
    result = await session.execute(select(User).where(User.tg_id == tg_id))
    return result.scalar_one_or_none()
