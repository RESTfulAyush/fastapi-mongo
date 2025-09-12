from fastapi import FastAPI
from routes import employees
from database import check_db_connection

app = FastAPI(title="CRUD API")

app.include_router(employees.router)

@app.on_event("startup")
async def startup_db_client():
    connected = await check_db_connection()
    if not connected:
        print("Could not connect to MongoDB")

@app.get("/")
async def root():
    return {"message": "Welcome"}
