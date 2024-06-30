from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from weather_app import models, schemas


async def get_city(db: AsyncSession, city_id: int):
    result = await db.execute(
        select(models.City).filter(models.City.id == city_id)
    )
    return result.scalars().first()


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def update_city(
    db: AsyncSession, city_id: int, city: schemas.CityCreate
):
    db_city = await get_city(db, city_id)
    if db_city is None:
        return None
    db_city.name = city.name
    db_city.additional_info = city.additional_info
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, city_id: int):
    db_city = await get_city(db, city_id)
    if db_city is None:
        return None
    await db.delete(db_city)
    await db.commit()
    return db_city


async def get_temperatures(
    db: AsyncSession, city_id: int = None
) -> Sequence[models.Temperature]:
    query = select(models.Temperature)
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)
    result = await db.execute(query)
    return result.scalars().all()


async def create_temperature(
    db: AsyncSession, temperature: schemas.TemperatureCreate
) -> models.Temperature:
    db_temperature = models.Temperature(**temperature.dict())
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature


async def get_cities(db: AsyncSession) -> Sequence[models.City]:
    result = await db.execute(select(models.City))
    return result.scalars().all()
