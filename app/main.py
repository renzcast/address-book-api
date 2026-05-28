from fastapi import FastAPI
from app.database import Base, engine, SessionLocal
from app.routes.address import router as address_router
from app.seed_data import seed_demo_data

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Initialize demo data
db = SessionLocal()
try:
    seed_demo_data(db)
finally:
    db.close()

app.include_router(address_router)