from pydantic import BaseModel


class BuildingBase(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float

    class Config:
        orm_mode = True


class OrganizationBase(BaseModel):
    id: int
    name: str
    phone_numbers: str
    building_id: int

    class Config:
        orm_mode = True
