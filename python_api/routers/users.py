from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas.user import UserCreate, UserOut, UserLogin
from ..schemas.error import ErrorResponse
from ..database import SessionLocal
from ..models.user import User
from passlib.context import CryptContext
from jose import jwt
import uuid
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..core.config import settings

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

from fastapi import Response


@router.post("/register", response_model=UserOut, status_code=201, responses={400: {"model": ErrorResponse}})
def register(user: UserCreate, db: Session = Depends(get_db), response: Response = None):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    try:
        # Provide a Location header for the created resource (informational)
        if response is not None:
            response.headers["Location"] = f"/auth/users/{db_user.id}"
    except Exception:
        pass
    return db_user

@router.post("/login", responses={200: {"description": "Authentication successful"}, 401: {"model": ErrorResponse}})
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_access_token(data={"sub": user.id, "type": "refresh"}, expires_delta=timedelta(days=7))
    return {
        "accessToken": access_token,
        "refreshToken": refresh_token,
        "expiresIn": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }
