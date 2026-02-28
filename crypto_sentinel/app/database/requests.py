from app.database.database import async_session
from app.database.models import User, Alerts
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

async def set_user(tg_id: int, username: str | None): #TODO: add in model first_name and last_name if user_name is None
    async with async_session() as session:
        user=await session.scalar(select(User).where(User.tg_id==tg_id))
        
        if not user:
            session.add(User(tg_id=tg_id, username=username))
            await session.commit()

async def add_alert(tg_id: int, symbol: str, target_price: float, direction: str):
    async with async_session() as session:
        user=await session.scalar(select(User).where(User.tg_id==tg_id))
        if user:
            alert = Alerts(user_id=user.id,
                        symbol=symbol.upper(),
                        target_price=target_price,
                        direction=direction,
                        is_active=True)
            session.add(alert)
            await session.commit()
            return True
        return False
    
async def get_user_alerts(tg_id: int):
    async with async_session() as session:
        query = select(Alerts).join(User).where(User.tg_id == tg_id)
        result = await session.execute(query)
        return result.scalars().all()
    
async def get_active_alerts(session: AsyncSession):
        query = select(Alerts).options(joinedload(Alerts.user)).where(Alerts.is_active == True)
        result = await session.execute(query)
        return result.scalars().all()

async def set_user_language(session, tg_id: int, lang_code: str):
    await session.execute(
        update(User)
        .where(User.tg_id == tg_id)
        .values(language=lang_code)
    )
    await session.commit()

async def get_user(tg_id: int, session: AsyncSession):
    result = await session.execute(select(User).where(User.tg_id == tg_id))
    return result.scalar_one_or_none()