from fastapi import APIRouter, HTTPException, Query
from database import employees_collection
from models import Employee, EmployeeUpdate

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.post("/")
async def create_employee(employee: Employee):
    print('employees: ', employee)
    existing = await employees_collection.find_one({"employee_id": employee.employee_id})
    if existing:
        raise HTTPException(status_code=400, detail="Employee ID already exists")
    await employees_collection.insert_one(employee.dict())
    return employee

@router.get("/")
async def get_employees(
    employee_id: str = Query(None, description="Employee ID to fetch a specific employee"),
    department: str = Query(None, description="Department to filter employees")
):
    if employee_id:
        employee = await employees_collection.find_one({"employee_id": employee_id})
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        employee["_id"] = str(employee["_id"])
        return employee

    query = {}
    if department:
        query["department"] = department

    data = employees_collection.find(query)

    employees = []
    async for employee in data:
        employee["_id"] = str(employee["_id"])
        employees.append(employee)
    if len(employees) == 0: return {"message": "No Employee found"}
    return employees


@router.put("/{employee_id}")
async def update_employee(employee_id: str, update_data: EmployeeUpdate):
    update_dict = update_data.dict(exclude_unset=True)

    if not update_dict:
        raise HTTPException(status_code=400, detail="Enter data")

    result = await employees_collection.update_one(
        {"employee_id": employee_id},
        {"$set": update_dict}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")

    updated_employee = await employees_collection.find_one({"employee_id": employee_id})
    updated_employee["_id"] = str(updated_employee["_id"])
    return updated_employee

@router.delete("/{employee_id}")
async def delete_employee(employee_id: str):
    result = await employees_collection.delete_one({"employee_id": employee_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")

    return {"detail": f"Employee {employee_id} deleted successfully"}


@router.get("/avg-salary")
async def get_avg_salary_by_department():
    pipeline = [
        {
            "$group": {
                "_id": "$department",
                "avg_salary": {"$avg": "$salary"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "department": "$_id",
                "avg_salary": {"$round": ["$avg_salary", 2]}
            }
        }
    ]
    
    data = employees_collection.aggregate(pipeline)
    result = []
    async for doc in data:
        result.append(doc)
    
    return result

@router.get("/search")
async def search_employees_by_skill(skill: str = Query(..., description="Skill")):
    if not skill:
        raise HTTPException(status_code=400, detail="No Skill Passed")

    data = employees_collection.find({"skills": {"$regex": skill, "$options": "i"}})
    employees = []
    async for employee in data:
        employee["_id"] = str(employee["_id"])
        employees.append(employee)

    return employees