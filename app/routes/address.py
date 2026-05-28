from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.address import Address
from app.schemas.address import AddressCreate, AddressResponse, AddressUpdate, NearbyAddressResponse, \
    AddressListResponse
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

    try:
        db.add(new_address)
        db.commit()
        db.refresh(new_address)

    except IntegrityError:
        db.rollback()

        logger.warning(
            "Duplicate coordinates detected "
            f"lat={address.latitude}, lon={address.longitude}"
        )

        raise HTTPException(
            status_code=409,
            detail="Address with these coordinates already exists"
        )

    except Exception as e:
        db.rollback()

        logger.exception("Unexpected database error during post operation")

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

    logger.info(f"Address created with id={new_address.id}")

    return new_address

@router.get("", response_model=AddressListResponse)
def get_addresses(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    logger.info(f"Fetching addresses limit={limit}, offset={offset}")

    total = db.query(Address).count()

    addresses = (
        db.query(Address).offset(offset)
        .limit(limit).all()
    )

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": addresses
    }

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


    try:
        db.commit()
        db.refresh(address)

    except IntegrityError:
        db.rollback()

        logger.warning(
            f"Duplicate coordinates on update id={address_id} "
            f"lat={address.latitude}, lon={address.longitude}"
        )

        raise HTTPException(
            status_code=409,
            detail="Another address already uses these coordinates"
        )

    except Exception as e:
        db.rollback()

        logger.exception("Unexpected database error during put operation")

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

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

    try:
        db.delete(address)
        db.commit()

    except Exception as e:
        db.rollback()

        logger.exception("Unexpected database error during delete operation")

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

    logger.info(f"Address deleted id={address_id}")

    return {"message": f"Address deleted id={address_id}"}

