from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    middle_name: str | None
    email: EmailStr
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}


class UserUpdateRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    is_active: bool | None = None
