# 📍 Address Book API (FastAPI)

This Address Book API showcases backend engineering skills using FastAPI, SQLAlchemy, and Pydantic, focusing on clean architecture and production-style API design.

It implements CRUD operations with pagination, geospatial nearby search, and database-level integrity constraints to ensure data consistency. The project emphasizes strong API design through structured request/response schemas, validation rules, and consistent error handling (including proper conflict handling for duplicate coordinates).

Beyond functionality, the repository highlights real-world engineering discipline through a Git workflow simulation, including feature branching, incremental commits, pull request-based integration, and code review-style refinements.

Overall, it demonstrates not just API development, but also how clean backend structure, data integrity, and professional development workflow practices come together in a production-like environment.

---

# 🚀 Features

- Create, update, delete addresses (CRUD)
- Retrieve all addresses
- Retrieve address by ID
- Geolocation-based nearby search (distance filtering)
- Input validation using Pydantic
- SQLite database integration using SQLAlchemy
- Structured logging
- Clean modular architecture
- Database mock data intialization

---

# 🧰 Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy (ORM)
- SQLite
- Pydantic
- Geopy (for distance calculation)
- Uvicorn

---

# 📦 Project Setup

## 1. Clone the Repository

```bash
git clone https://github.com/renzcast/address-book-api
cd address-book-api
```

---

## 2. Create Virtual Environment

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=sqlite:///./addresses.db
```

---

## 5. Run the Application

```bash
uvicorn app.main:app --reload
```

---

## 6. Access API Documentation

- Swagger UI: http://127.0.0.1:8000/docs  
- ReDoc: http://127.0.0.1:8000/redoc  

---

# 📡 API Endpoints

## Create Address
POST /api/v1/addresses
```json
{
  "name": "string",
  "street": "string",
  "city": "string",
  "latitude": -90,
  "longitude": -180
}
```
## Get All Addresses
GET /api/v1/addresses
```json
{
  "total": 0,
  "limit": 0,
  "offset": 0,
  "items": [
    {
      "name": "string",
      "street": "string",
      "city": "string",
      "latitude": -90,
      "longitude": -180,
      "id": 0,
      "created_at": "2026-05-28T18:26:15.146Z",
      "updated_at": "2026-05-28T18:26:15.146Z"
    }
  ]
}
```
## Get Address by ID
GET /api/v1/addresses/{address_id}
```json
{
  "name": "string",
  "street": "string",
  "city": "string",
  "latitude": -90,
  "longitude": -180,
  "id": 0,
  "created_at": "2026-05-28T18:27:09.553Z",
  "updated_at": "2026-05-28T18:27:09.553Z"
}
```
## Update Address
PUT /api/v1/addresses/{address_id}
```json
{
  "name": "string",
  "street": "string",
  "city": "string",
  "latitude": -90,
  "longitude": -180
}
```
## Delete Address
DELETE /api/v1/addresses/{address_id}

## Nearby Search
GET /api/v1/addresses/nearby?lat={lat}&lon={lon}&distance={km}
```json
[
  {
    "name": "string",
    "street": "string",
    "city": "string",
    "latitude": -90,
    "longitude": -180,
    "id": 0,
    "created_at": "2026-05-28T18:26:56.618Z",
    "updated_at": "2026-05-28T18:26:56.618Z",
    "distance_km": 0
  }
]
```
---

# 🧠 Design Decisions

- SQLAlchemy ORM used for maintainable database operations
- Pydantic validation ensures invalid data is rejected early
- Geopy library used for accurate geospatial distance calculation
- Modular architecture separates routes, models, schemas, and services
- SQLite chosen for simplicity and portability

---

# 🧪 Future Improvements (Optional)

- Add authentication (JWT)
- Add unit tests (pytest)
- Add Docker support
- Add request/response caching

---

# 🧾 Version Control Highlights

This project demonstrates:

- Incremental feature development
- Structured commit history
- Feature branching and merging workflow
- Iterative improvements based on debugging and review

---

# 📌 Notes

- Database file (.db) is excluded from version control
- Environment variables are managed via .env
- Swagger UI is used for testing endpoints
