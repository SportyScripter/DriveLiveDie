from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from auth.models import User
from schemas.vehicle import UserVehicle
from models.vehicle import Vehicle
import requests
import json
from auth.utils import get_current_active_user
from typing import Annotated
from enum import Enum


vehicle_router = APIRouter(prefix="/select", tags=["vehicle"])


class CarYear(str, Enum):
    a = "2015"
    b = "2016"
    c = "2017"
    d = "2018"
    e = "2019"
    f = "2020"


def get_makes(car_year: CarYear):
    year = car_year.value
    path = f"https://carapi.app/api/makes?year={year}"
    response = requests.get(path)
    if response.status_code == 200:
        data = json.loads(response.text)
        data = data["data"]
        for j in range(len(data) - 1):
            for i in range(len(data) - 1):
                if int(data[i]["id"]) > int(data[i + 1]["id"]):
                    temp = data[i]
                    data[i] = data[i + 1]
                    data[i + 1] = temp
        return data
    else:
        return f"Błąd:  {response.status_code}"


def get_models(make_id, make, year):
    path = f"https://carapi.app/api/models?year={year}&make={make}&make_id={make_id}"
    response = requests.get(path)
    if response.status_code == 200:
        data = json.loads(response.text)
        data = data["data"]
        return data
    else:
        return f"Błąd: {response.status_code}"


def get_trims(year, make, model, make_model_id, make_id):
    path = f"https://carapi.app/api/trims?year={year}&make={make}&model={model}&make_model_id={make_model_id}&make_id={make_id}"
    response = requests.get(path)
    if response.status_code == 200:
        data = json.loads(response.text)
        data = data["data"]
        return data
    return f"Błąd: {response.status_code}"


def get_colour(trim_id):
    path = f"https://carapi.app/api/trims/{trim_id}"
    response = requests.get(path)
    if response.status_code == 200:
        data = json.loads(response.text)
        data = data["make_model_trim_interior_colors"]
        return data
    return f"Błąd: {response.status_code}"


@vehicle_router.post("/year/{car_year}")
async def select_vehicle_year(
    car_year: CarYear,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    try:
        new_vehicle = Vehicle(year=car_year.value, user_id=current_user.id)
        db.add(new_vehicle)
        db.commit()
        db.refresh(new_vehicle)
        car_list = get_makes(car_year)
        return car_list
    except Exception as e:
        raise HTTPException(status_code=403, detail="CSRF token verification failed")


@vehicle_router.post("/models/{make_id}/{make}")
async def select_vehicle_model(
    make_id: int,
    make: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    try:
        vehicle = (
            db.query(Vehicle)
            .filter_by(user_id=current_user.id)
            .order_by(Vehicle.id.desc())
            .first()
        )
        if not vehicle:
            raise HTTPException(status_code=400, datail="Start to begining")
        car_list_of_models = get_models(make_id=make_id, make=make, year=vehicle.year)
        if not car_list_of_models:
            raise HTTPException(status_code=400, detail="Vahicle idn't exists")
        vehicle.make = make
        vehicle.make_id = make_id
        db.commit()
        db.refresh(vehicle)
        return car_list_of_models
    except Exception as e:
        raise HTTPException(status_code=403, detail="CSRF token verification failed")


@vehicle_router.post("/trims/{make_model_id}/{model}")
async def select_vehicle_trim(
    make_model_id: str,
    model: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    try:
        vehicle = (
            db.query(Vehicle)
            .filter_by(user_id=current_user.id)
            .order_by(Vehicle.id.desc())
            .first()
        )
        if not vehicle:
            raise HTTPException(status_code=400, detail="Start to begining")
        car_list_of_trims = get_trims(
            year=vehicle.year,
            make=vehicle.make,
            model=model,
            make_model_id=make_model_id,
            make_id=vehicle.make_id,
        )
        vehicle.model = model
        vehicle.make_model_id = make_model_id
        db.commit()
        db.refresh(vehicle)
        return car_list_of_trims
    except Exception as e:
        raise HTTPException(status_code=403, detail="CSRF token verification failed")


@vehicle_router.post(
    "/colour/{trim_id}/{trim_name}/{trim_description}/{msrp}/{invoice}"
)
async def select_vehicle_trim(
    trim_id: int,
    trim_name: str,
    trim_description: str,
    msrp: int,
    invoice: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    try:
        vehicle = (
            db.query(Vehicle)
            .filter_by(user_id=current_user.id)
            .order_by(Vehicle.id.desc())
            .first()
        )
        if not vehicle:
            raise HTTPException(status_code=400, detail="Start to begining")
        car_list_of_colour = get_colour(trim_id=trim_id)
        vehicle.trim_id = trim_id
        vehicle.trim_name = trim_name
        vehicle.trim_description = trim_description
        vehicle.msrp = msrp
        vehicle.invoice = invoice
        db.commit()
        db.refresh(vehicle)
        return car_list_of_colour
    except Exception as e:
        raise HTTPException(status_code=403, detail="CSRF token verification failed")


@vehicle_router.post("/interior/{interior_description}/{rgb}")
async def select_vehicle_interior(
    interior_description: str,
    rgb: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    try:
        vehicle = (
            db.query(Vehicle)
            .filter_by(user_id=current_user.id)
            .order_by(Vehicle.id.desc())
            .first()
        )
        if not vehicle:
            raise HTTPException(status_code=400, detail="Start to begining")
        vehicle.interior = interior_description
        vehicle.rgb = rgb
        db.commit()
        db.refresh(vehicle)
        user_vehicle = UserVehicle(
            year=vehicle.year,
            make=vehicle.make,
            model=vehicle.model,
            trim_name=vehicle.trim_name,
            trim_description=vehicle.trim_description,
            msrp=vehicle.msrp,
            invoice=vehicle.invoice,
            interior=vehicle.interior,
            rgb=vehicle.rgb,
        )
        return user_vehicle
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))
