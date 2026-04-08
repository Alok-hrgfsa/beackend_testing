from pydantic import BaseModel, EmailStr
from typing import Optional, Any

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    employee_number: str
    email: EmailStr
    password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class StandardResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None