from pydantic import BaseModel, Field
from typing import Optional


class AddressBase(BaseModel):
    name: str
    street: Optional[str] = None
    city: Optional[str] = None
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    name: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)


class AddressResponse(AddressBase):
    id: int

    class Config:
        from_attributes = True