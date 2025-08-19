from fastapi import APIRouter, Depends, HTTPException, status

from src.features.users.schemas import UserCreate, UserRead, UserUpdate
from src.features.users.use_cases import UserUseCase, get_user_use_case

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
async def get_all(use_case: UserUseCase = Depends(get_user_use_case)):
    return await use_case.get_all()


@router.get("/{user_id}", response_model=UserRead)
async def get_by_id(user_id: int, use_case: UserUseCase = Depends(get_user_use_case)):
    user = await use_case.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.post("/", response_model=UserRead)
async def create_user(
    user_in: UserCreate, use_case: UserUseCase = Depends(get_user_use_case)
):
    user = await use_case.create_user(user_in)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User could not be created"
        )
    return user


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, use_case: UserUseCase = Depends(get_user_use_case)):
    if not await use_case.delete_user(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    use_case: UserUseCase = Depends(get_user_use_case),
):
    return await use_case.update_user(user_id, user_in)
