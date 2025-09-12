from fastapi import APIRouter, HTTPException
from database import employees_collection
from models import Employee

router = APIRouter(prefix="/employees", tags=["Employees"])

# Create Employee
@router.post("/")
async def create_employee(employee: Employee):
    print('employees: ', employee)
    existing = await employees_collection.find_one({"employee_id": employee.employee_id})
    if existing:
        raise HTTPException(status_code=400, detail="Employee ID already exists")
    await employees_collection.insert_one(employee.dict())
    return employee

# Get Employee
@router.get("/{employee_id}")
async def get_employee(employee_id: str):
    employee = await employees_collection.find_one({"employee_id": employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    employee["_id"] = str(employee["_id"])  # convert ObjectId
    return employee
