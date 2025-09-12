from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Employee(BaseModel):
    employee_id: str
    name: str
    department: Optional[str] = None
    salary: Optional[float] = None
    joining_date: Optional[datetime] = None
    skills: Optional[List[str]] = []
