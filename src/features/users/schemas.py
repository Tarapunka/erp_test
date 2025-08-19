from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True


class UserCreate(UserBase):
    password: str
    is_superuser: bool

    model_config = ConfigDict(extra="forbid")


class UserRead(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None
    is_superuser: bool = False

    model_config = ConfigDict(extra="forbid")
