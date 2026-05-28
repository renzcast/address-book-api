from sqlalchemy.orm import Session
from app.models.address import Address
from app.utils.logger import logger

demo_addresses = [
    {
        "name": "SM North EDSA",
        "street": "North Avenue",
        "city": "Quezon City",
        "latitude": 14.6567,
        "longitude": 121.0307
    },
    {
        "name": "Trinoma",
        "street": "North Avenue",
        "city": "Quezon City",
        "latitude": 14.6536,
        "longitude": 121.0348
    },
    {
        "name": "Eastwood City",
        "street": "E. Rodriguez Jr. Ave",
        "city": "Quezon City",
        "latitude": 14.6103,
        "longitude": 121.0796
    },
    {
        "name": "UP Town Center",
        "street": "Katipunan Ave",
        "city": "Quezon City",
        "latitude": 14.6579,
        "longitude": 121.0745
    },
    {
        "name": "SM Megamall",
        "street": "EDSA",
        "city": "Mandaluyong",
        "latitude": 14.5856,
        "longitude": 121.0566
    },
    {
        "name": "Shangri-La Plaza",
        "street": "EDSA",
        "city": "Mandaluyong",
        "latitude": 14.5825,
        "longitude": 121.0539
    },
    {
        "name": "Ayala Triangle Gardens",
        "street": "Ayala Ave",
        "city": "Makati",
        "latitude": 14.5533,
        "longitude": 121.0248
    },
    {
        "name": "Glorietta",
        "street": "Ayala Center",
        "city": "Makati",
        "latitude": 14.5515,
        "longitude": 121.0229
    },
    {
        "name": "Bonifacio High Street",
        "street": "BGC",
        "city": "Taguig",
        "latitude": 14.5514,
        "longitude": 121.0479
    },
    {
        "name": "Market! Market!",
        "street": "BGC",
        "city": "Taguig",
        "latitude": 14.5491,
        "longitude": 121.0507
    }
]


def seed_demo_data(db: Session):

    existing_addresses = db.query(Address).count()

    # Prevent duplicate seeding
    if existing_addresses > 0:
        return

    for address_data in demo_addresses:
        address = Address(**address_data)
        db.add(address)

    db.commit()

    logger.info("Demo mock data initialized")
