from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets

from app.database import get_db
from app.models.user import User
from app.schemas.auth import (
    LoginRequest, RegisterRequest,
    ForgotPasswordRequest, ResetPasswordRequest,
    StandardResponse
)
from app.utils.security import hash_password, verify_password
from app.utils.jwt_utils import create_access_token
from app.services.email_service import send_reset_email

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login", response_model=StandardResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.hashed_password):
        return StandardResponse(success=False, message="Invalid credentials")

    token = create_access_token({"sub": str(user.id), "email": user.email, "role": user.role })
    return StandardResponse(
        success=True,
        message="Login successful",
        data={
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "employee_number": user.employee_number,
                    "role": user.role 
            }
        }
    )

@router.post("/register", response_model=StandardResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == req.email).first():
        return StandardResponse(success=False, message="Email already registered")
    if db.query(User).filter(User.employee_number == req.employee_number).first():
        return StandardResponse(success=False, message="Employee number already in use")

    user = User(
        email=req.email,
        employee_number=req.employee_number,
        hashed_password=hash_password(req.password),
        role="user" 
    )
    db.add(user)
    db.commit()
    return StandardResponse(success=True, message="Registration successful")

@router.post("/forgot-password", response_model=StandardResponse)
async def forgot_password(req: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if user:
        token = secrets.token_urlsafe(32)
        user.reset_token = token
        user.reset_token_expiry = datetime.utcnow() + timedelta(minutes=30)
        db.commit()
        await send_reset_email(user.email, token)

    return StandardResponse(
        success=True,
        message="If that email is registered, a reset link has been sent."
    )

@router.post("/reset-password", response_model=StandardResponse)
def reset_password(req: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.reset_token == req.token).first()
    if not user or user.reset_token_expiry < datetime.utcnow():
        return StandardResponse(success=False, message="Invalid or expired token")

    user.hashed_password = hash_password(req.new_password)
    user.reset_token = None
    user.reset_token_expiry = None
    db.commit()
    return StandardResponse(success=True, message="Password reset successful")