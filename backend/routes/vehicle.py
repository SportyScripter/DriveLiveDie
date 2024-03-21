from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from auth.models import User, Token
from auth.auth_bearer import JWTBearer
from schemas.vehicle import VehicleYear
from models.vehicle import Vehicle
import requests
import json 
from auth.utils import get_current_active_user
from typing import Annotated
vehicle_router = APIRouter(prefix="/select", tags=["vehicle"])
from enum import Enum

class CarYear(str,Enum):
    a = "2015"
    b = "2016"
    c = "2017"
    d = "2018"
    e = "2019"
    f = "2020"


def get_makes(car_year : CarYear):
    year = car_year.value
    path = f'https://carapi.app/api/makes?year={year}'
    response = requests.get(path)
    if response.status_code == 200:
        data = json.loads(response.text)
        data = data['data']
        for j in range(len(data)-1):
            for i in range(len(data)-1):
                if int(data[i]['id']) > int(data[i+1]["id"]):
                    temp = data[i]
                    data[i] = data[i+1]
                    data[i+1] = temp
        return data
    else:
        return f"Błąd:  {response.status_code}"

def get_models(make_id,make,year):
    path = f'https://carapi.app/api/models?year={year}&make={make}&make_id={make_id}'
    response = requests.get(path)
    if response.status_code == 200:
        data = json.loads(response.text)
        data = data['data']
        return data
    else:
        return f"Błąd: {response.status_code}"    


    
@vehicle_router.post("/year/{car_year}")
async def select_vehicle_year(car_year : CarYear,current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    new_vehicle = Vehicle(year = car_year.value, user_id = current_user.id)
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    car_list = get_makes(car_year)
    return car_list


    

@vehicle_router.post("/models/{make_id}/{make}")
async def select_vehicle_model(make_id : int, make : str,current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    try:
        vehicle = db.query(Vehicle).filter_by(user_id = current_user.id).order_by(Vehicle.id.desc()).first()
        if not vehicle:
            raise HTTPException(status_code=400 , datail="Start to begining")
        car_list_of_models = get_models(make_id=make_id,make=make,year=vehicle.year)
        if not car_list_of_models:
            raise HTTPException(status_code=400 , detail="Vahicle idn't exists")
        vehicle.make = make
        vehicle.make_id = make_id
        db.commit()
        db.refresh(vehicle)
        return car_list_of_models
    except Exception as e:
        raise HTTPException(status_code=403, detail="CSRF token verification failed")
