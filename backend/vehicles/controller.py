from fastapi import Depends, APIRouter, HTTPException, status

vehicles_controller = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@vehicles_controller.get("/")
def get_vehicles():
    return 
