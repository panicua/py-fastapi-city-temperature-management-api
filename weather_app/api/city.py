from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from weather_app import crud, schemas

router = APIRouter()


@router.post("/cities/", response_model=schemas.CityOut)
async def create_city(
    city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.create_city(db=db, city=city)


@router.get("/cities/", response_model=List[schemas.CityOut])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_cities(db)


@router.get("/cities/{city_id}", response_model=schemas.CityOut)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.put("/cities/{city_id}", response_model=schemas.CityOut)
async def update_city(
    city_id: int, city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
):
    db_city = await crud.update_city(db, city_id=city_id, city=city)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.delete("/cities/{city_id}", response_model=schemas.CityOut)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.delete_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city
