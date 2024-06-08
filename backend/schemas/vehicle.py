from pydantic import BaseModel


class UserVehicle(BaseModel):
    year: int
    make: str
    model: str
    trim_name: str
    trim_description: str
    msrp: int
    invoice: int
    interior: str
    rgb: str

UserVehicle.update_forward_refs()