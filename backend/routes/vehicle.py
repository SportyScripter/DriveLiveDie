from fastapi import Depends, APIRouter, HTTPException
# from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.auth.models import User, Token
from backend.auth.auth_bearer import JWTBearer
from backend.schemas.vehicle import VehicleYear
from backend.models.vehicle import vehicle
vehicle_router = APIRouter(prefix="/select", tags=["vehicle"])
from requests import Request as request


def get_models(year):
    models = request(url = f'https://carapi.app/api/makes?year={year}')
    print(type(models))
    print(models)
    return models

cars = get_models(2016)
print(cars)


@vehicle_router.post("/year")
async def select_vehicle_year(name : str):
    name = "Hello_world"
    return name
