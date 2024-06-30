from fastapi import FastAPI

from database import engine, Base
from weather_app.api import city, temperature

app = FastAPI()

# Include the routers
app.include_router(city.router, prefix="/api", tags=["cities"])
app.include_router(temperature.router, prefix="/api", tags=["temperatures"])


@app.on_event("startup")
async def startup():
    # Run Alembic migrations
    import subprocess
    subprocess.run(["alembic", "upgrade", "head"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the City Temperature Management API"}

