from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class AddressListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[AddressResponse]

class NearbyAddressResponse(AddressResponse):
    distance_km: float