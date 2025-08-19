from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from .use_cases import TaskUseCase, get_task_use_case
from .schemas import TaskCreate, TaskRead

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=List[TaskRead])
async def get_all(
    use_case: TaskUseCase = Depends(get_task_use_case),
):
    return await use_case.get_all()


@router.get("/created-by/{creater_id}")
async def get_by_creater(
    creater_id: int,
    use_case: TaskUseCase = Depends(get_task_use_case),
):
    return await use_case.get_by_creater(creater_id)


@router.get("/assigned-to/{assignee_id}")
async def get_by_assigned(
    assignee_id: int,
    use_case: TaskUseCase = Depends(get_task_use_case),
):
    return await use_case.get_by_assigned(assignee_id)


@router.get("/my-assigned")
async def get_my_assigned(
    user_id: int,  # TODO добавть get_current_user
    use_case: TaskUseCase = Depends(get_task_use_case),
):
    pass


@router.post("/", response_model=TaskRead)
async def create_task(
    task_in: TaskCreate,
    use_case: TaskUseCase = Depends(get_task_use_case),
):
    return await use_case.create_task(task_in)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    task_id: int,
    use_case: TaskUseCase = Depends(get_task_use_case),
):
    if not await use_case.delete_task(task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return None
