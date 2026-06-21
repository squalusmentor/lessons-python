from pydantic import BaseModel, EmailStr


class SignUpRequest(BaseModel):
    first_name: str
    last_name: str
    middle_name: str | None = None
    email: EmailStr
    password: str
    password_confirm: str


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    message: str
