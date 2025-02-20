from fastapi import APIRouter, HTTPException, Query
from typing import Annotated, Optional
from ..models import Employee
from .utils import get_response_object, generate_filters

employee_router = APIRouter(prefix="/employees", tags=["Employees"])

@employee_router.post("")
async def create_employee(employee: Employee):
    return {"data": await employee.insert()}


@employee_router.get("")
async def get_employees(
    page: int,
    size: int,
    id: Optional[str] = None,
    first_name: Annotated[str | None, Query(min_length=1)] = None,
    last_name: Annotated[str | None, Query(min_length=1)] = None,
    register_code: Optional[int] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = Query("asc", regex="^(asc|desc)$"),
):
    filters = generate_filters(locals().items())
    query = Employee.find(filters)

    if sort_by:
        sort_direction = 1 if sort_order == "asc" else -1
        query = query.sort((sort_by, sort_direction))
    
    total_count = await query.count()
    employees = await query.skip((page - 1) * size).limit(size).to_list()

    return get_response_object(employees, page, size, total_count)


@employee_router.put("/{id}")
async def update_employee(id: str, employee_update: Employee):
    employee = await Employee.get(id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    update_data = employee_update.dict(exclude_unset=True)
    await employee.set(update_data)

    return {"data": employee}


@employee_router.delete("/{id}")
async def delete_employee(id: str):
    employee = await Employee.get(id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    await employee.delete()
    return {"message": "Employee deleted successfully"}
