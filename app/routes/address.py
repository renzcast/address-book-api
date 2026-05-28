from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.address import Address
from app.schemas.address import AddressCreate, AddressResponse, AddressUpdate, NearbyAddressResponse
from app.utils.logger import logger
from geopy.distance import geodesic


router = APIRouter(
    prefix="/api/v1/addresses",
    tags=["Addresses"]
)

@router.post("", response_model=AddressResponse)
def create_address(
        address: AddressCreate,
        db: Session = Depends(get_db)
):
    logger.info("Creating new address")

    new_address = Address(
        name=address.name,
        street=address.street,
        city=address.city,
        latitude=address.latitude,
        longitude=address.longitude
    )

    db.add(new_address)
    db.commit()
    db.refresh(new_address)

    logger.info(f"Address created with id={new_address.id}")

    return new_address

@router.get("", response_model=list[AddressResponse])
def get_addresses(db: Session = Depends(get_db)):

    logger.info("Fetching all addresses")

    return db.query(Address).all()

@router.get("/nearby", response_model=list[NearbyAddressResponse], response_model_exclude_none=True)
def nearby_addresses(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    distance_km: float = Query(..., gt=0),
    db: Session = Depends(get_db)
):
    logger.info(
        f"Searching nearby addresses "
        f"lat={lat}, lon={lon}, distance_km={distance_km}"
    )

    addresses = db.query(Address).all()

    nearby_results = []

    for address in addresses:

        # Skip addresses without coordinates
        if address.latitude is None or address.longitude is None:
            continue

        distance = geodesic(
            (lat, lon),
            (address.latitude, address.longitude)
        ).km

        if distance <= distance_km:
            nearby_results.append({
                "id": address.id,
                "name": address.name,
                "street": address.street,
                "city": address.city,
                "latitude": address.latitude,
                "longitude": address.longitude,
                "distance_km": round(distance, 2)
            })

    logger.info(f"Found {len(nearby_results)} nearby addresses")

    return nearby_results

@router.get("/{address_id}", response_model=AddressResponse)
def get_address(address_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching address with id={address_id}")

    address = db.query(Address).filter(Address.id == address_id).first()

    if not address:
        logger.warning(f"Address not found id={address_id}")
        raise HTTPException(
            status_code=404,
            detail=f"Address not found id={address_id}"
        )

    return address

@router.put("/{address_id}", response_model=AddressResponse)
def update_address(
    address_id: int,
    address_update: AddressUpdate,
    db: Session = Depends(get_db)
):
    logger.info(f"Updating address id={address_id}")

    address = db.query(Address).filter(Address.id == address_id).first()

    if not address:
        logger.warning(f"Address not found id={address_id}")
        raise HTTPException(
            status_code=404,
            detail=f"Address not found id={address_id}"
        )

    update_data = address_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(address, key, value)

    db.commit()
    db.refresh(address)

    logger.info(f"Address updated id={address_id}")

    return address

@router.delete("/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting address id={address_id}")

    address = db.query(Address).filter(Address.id == address_id).first()

    if not address:
        logger.warning(f"Address not found id={address_id}")
        raise HTTPException(
            status_code=404,
            detail=f"Address not found id={address_id}"
        )

    db.delete(address)
    db.commit()

    logger.info(f"Address deleted id={address_id}")

    return {"message": f"Address deleted id={address_id}"}

