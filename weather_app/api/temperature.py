import asyncio
from datetime import datetime
from typing import Dict, Any, Callable, Sequence

import httpx
from decouple import config
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from tenacity import retry, stop_after_attempt, wait_fixed

from database import SessionLocal, get_db
from weather_app import crud, schemas, models

router = APIRouter()

WEATHER_API_KEY = config("WEATHER_API_KEY", default=None)
WEATHER_API_URL = config("WEATHER_API_URL",
                         default="http://api.weatherapi.com/v1/current.json")

if WEATHER_API_KEY is None or WEATHER_API_URL is None:
    raise ValueError("WEATHER_API_KEY and WEATHER_API_URL must be set")


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def fetch_weather(
    client: httpx.AsyncClient, city_name: str
) -> Dict[str, Any]:
    response = await client.get(
        WEATHER_API_URL, params={"key": WEATHER_API_KEY, "q": city_name}
    )
    response.raise_for_status()
    return response.json()


async def process_city(
    client: httpx.AsyncClient,
    city: models.City,
    db_session_factory: Callable[[], AsyncSession],
) -> None:
    try:
        data = await fetch_weather(client, city.name)
        temperature = schemas.TemperatureCreate(
            city_id=city.id,
            date_time=datetime.now(),
            temperature=data["current"]["temp_c"],
        )
        async with db_session_factory() as new_db_session:
            await crud.create_temperature(new_db_session, temperature)
    except httpx.HTTPStatusError as exc:
        print(
            f"Error response {exc.response.status_code} "
            f"while requesting {exc.request.url!r}."
        )
    except Exception as e:
        print(f"An error occurred: {str(e)}")


@router.post("/temperatures/update/")
async def update_temperatures(db: AsyncSession = Depends(get_db)) -> dict:
    cities = await crud.get_cities(db)
    limits = httpx.Limits(max_connections=10, max_keepalive_connections=5)
    timeout = httpx.Timeout(10.0, connect=60.0)

    async with httpx.AsyncClient(limits=limits, timeout=timeout) as client:
        tasks = [process_city(client, city, SessionLocal) for city in cities]
        await asyncio.gather(*tasks)

    return {"status": "success"}


@router.get("/temperatures", response_model=list[schemas.Temperature])
async def read_temperatures(
    db: AsyncSession = Depends(get_db),
) -> Sequence[schemas.Temperature]:
    temperatures = await crud.get_temperatures(db)
    if not temperatures:
        raise HTTPException(status_code=404, detail="No temperatures found")
    return temperatures


@router.get(
    "/temperatures/{city_id}", response_model=list[schemas.Temperature]
)
async def read_temperature_by_city_id(
    city_id: int, db: AsyncSession = Depends(get_db)
) -> Sequence[schemas.Temperature]:
    temperatures = await crud.get_temperatures(db, city_id)
    if not temperatures:
        raise HTTPException(
            status_code=404,
            detail=f"No temperatures found for city ID {city_id}",
        )
    return temperatures
