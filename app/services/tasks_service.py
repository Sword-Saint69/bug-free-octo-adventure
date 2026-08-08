import uuid
from typing import List, Optional
from app.schemas.dashboard import TaskItem

class TasksService:
    """
    Dynamic Tasks Engine Service:
    Ee service-il user dynamic aayi add cheyyunna task items memory-il store cheyth handle cheyyunnu.
    Default aayi dynamic task fallbacks zero aanu (user add cheythaal mathram fill aakum).
    """
    _tasks: List[TaskItem] = []

    @classmethod
    async def get_user_tasks(cls) -> List[TaskItem]:
        return cls._tasks

    @classmethod
    async def create_task(cls, title: str, priority: str = "medium", due_time: Optional[str] = None) -> TaskItem:
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        new_task = TaskItem(
            id=task_id,
            title=title,
            completed=False,
            priority=priority,
            due_time=due_time
        )
        cls._tasks.insert(0, new_task)
        return new_task

    @classmethod
    async def toggle_task(cls, task_id: str) -> Optional[TaskItem]:
        for task in cls._tasks:
            if task.id == task_id:
                task.completed = not task.completed
                return task
        return None

    @classmethod
    async def delete_task(cls, task_id: str) -> bool:
        for i, task in enumerate(cls._tasks):
            if task.id == task_id:
                cls._tasks.pop(i)
                return True
        return False
