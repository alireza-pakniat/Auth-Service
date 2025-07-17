from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.context import CryptContext

from app.jwt_utils import create_access_token, verify_token
from typing import List

from sqlalchemy.orm import Session
from app.database import SessionLocal, User as DBUser


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users_db = {}  # Temporary in-memory user store

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class User(BaseModel):
    username: str
    password: str


class RegisterUser(BaseModel):
    username: str
    password: str
    role: str = "user"  # default role


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload  # contains "sub" (username) and "role"


def require_roles(roles: List[str]):
    def wrapper(user=Depends(get_current_user)):
        if user["role"] not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user

    return wrapper


@router.post("/register")
def register(user: RegisterUser, db: Session = Depends(get_db)):
    existing = db.query(DBUser).filter(DBUser.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_pw = pwd_context.hash(user.password)
    db_user = DBUser(username=user.username, hashed_password=hashed_pw, role=user.role)
    db.add(db_user)
    db.commit()
    return {"msg": f"User '{user.username}' registered as '{user.role}'"}


@router.post("/login", response_model=TokenResponse)
def login(user: User, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.username == user.username).first()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.username, "role": db_user.role})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/logout")
def logout():
    # In real JWT systems, client deletes token.
    return {"msg": "Logout (client-side only, token will expire in time)"}


@router.get("/admin-only")
def admin_area(user=Depends(require_roles(["admin"]))):
    return {"msg": f"Welcome admin {user['sub']}"}
