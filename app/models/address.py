from sqlalchemy import Column, Float, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from app.database import Base


class Address(Base):
    __tablename__ = "addresses"

    __table_args__ = (
        UniqueConstraint(
            "latitude",
            "longitude",
            name="uq_address_coordinates"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    street = Column(String, nullable=True)
    city = Column(String, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )