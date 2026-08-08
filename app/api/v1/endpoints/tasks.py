import uuid
from typing import List, Optional
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status
from app.schemas.response import StandardResponse
from app.schemas.dashboard import TaskItem
from app.services.tasks_service import TasksService

router = APIRouter()

class CreateTaskRequest(BaseModel):
    title: str
    priority: str = "medium"
    due_time: Optional[str] = None

@router.get("/tasks", response_model=StandardResponse[List[TaskItem]], summary="Fetch Dynamic Tasks")
async def get_tasks():
    tasks = await TasksService.get_user_tasks()
    return StandardResponse(
        request_id=f"req_{uuid.uuid4().hex[:10]}",
        data=tasks
    )

@router.post("/tasks", response_model=StandardResponse[TaskItem], status_code=status.HTTP_201_CREATED, summary="Create Dynamic Task")
async def create_task(payload: CreateTaskRequest):
    if not payload.title.strip():
        raise HTTPException(status_code=400, detail="Task title empty aayi nalkaan pattilla.")
    
    new_task = await TasksService.create_task(
        title=payload.title.strip(),
        priority=payload.priority,
        due_time=payload.due_time
    )
    return StandardResponse(
        request_id=f"req_{uuid.uuid4().hex[:10]}",
        data=new_task
    )

@router.patch("/tasks/{task_id}/toggle", response_model=StandardResponse[TaskItem], summary="Toggle Task Completion")
async def toggle_task(task_id: str):
    updated = await TasksService.toggle_task(task_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Task kandethan kazhinjilla")
    return StandardResponse(
        request_id=f"req_{uuid.uuid4().hex[:10]}",
        data=updated
    )

@router.delete("/tasks/{task_id}", response_model=StandardResponse[dict], summary="Delete Dynamic Task")
async def delete_task(task_id: str):
    success = await TasksService.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task kandethan kazhinjilla")
    return StandardResponse(
        request_id=f"req_{uuid.uuid4().hex[:10]}",
        data={"deleted_task_id": task_id, "success": True}
    )
