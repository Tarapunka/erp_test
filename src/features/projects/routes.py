from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from src.features.projects.use_case import ProjectUseCase, get_project_use_case
from src.features.projects.schemas import ProjectCreate, ProjectRead

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/", response_model=List[ProjectRead])
async def get_all(
    use_case: ProjectUseCase = Depends(get_project_use_case),
):
    return await use_case.get_all()


@router.get("/created-by/{creater_id}")
async def get_by_creater(
    creater_id: int,
    use_case: ProjectUseCase = Depends(get_project_use_case),
):
    return await use_case.get_by_creator(creater_id)


@router.get("/my-projects")
async def get_my_projects(
    user_id: int,  # TODO добавть get_current_user
    use_case: ProjectUseCase = Depends(get_project_use_case),
):
    pass


@router.post("/", response_model=ProjectRead)
async def create_project(
    task_in: ProjectCreate,
    use_case: ProjectUseCase = Depends(get_project_use_case),
):
    return await use_case.create_task(task_in)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    task_id: int,
    use_case: ProjectUseCase = Depends(get_project_use_case),
):
    if not await use_case.delete_task(task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return None
