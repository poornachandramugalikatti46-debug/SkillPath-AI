import os
import re
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage

import bcrypt
import jwt
from bson import ObjectId
from dotenv import load_dotenv
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from pydantic import BaseModel, Field
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

load_dotenv()

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
JWT_SECRET = os.getenv("JWT_SECRET", "")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "1440"))
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_APP_PASSWORD = os.getenv("SMTP_APP_PASSWORD")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

if not JWT_SECRET or JWT_SECRET == "REPLACE_WITH_A_LONG_RANDOM_SECRET":
    raise RuntimeError("Set a secure JWT_SECRET in your .env file.")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client["skillpath_ai"]
users = db["users"]
users.create_index("email", unique=True)

bearer_scheme = HTTPBearer(auto_error=False)


class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=8, max_length=128)


class GoogleRequest(BaseModel):
    credential: str = Field(..., min_length=10)


def normalize_email(email: str) -> str:
    return (email or "").strip().lower()


def password_is_valid(password: str) -> bool:
    return bool(
        len(password) >= 8
        and re.search(r"[a-z]", password)
        and re.search(r"[A-Z]", password)
        and re.search(r"\d", password)
    )


def serialize_user(user: dict) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user.get("name") or "Student",
        "email": user.get("email"),
        "provider": user.get("provider", "local"),
        "created_at": user.get("created_at").isoformat() if user.get("created_at") else None,
    }


def create_token(user: dict) -> str:
    payload = {
        "sub": str(user["_id"]),
        "email": user["email"],
        "name": user.get("name", "Student"),
        "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def send_welcome_email(name: str, email: str):
    try:
        if not all([SMTP_HOST, SMTP_EMAIL, SMTP_APP_PASSWORD]):
            return

        message = EmailMessage()
        message["Subject"] = "Welcome to SkillPath-AI"
        message["From"] = SMTP_EMAIL
        message["To"] = email
        message.set_content(
            (
                f"Hi {name},\n\n"
                "Your SkillPath-AI account has been created successfully.\n"
                "You can now log in and continue your learning journey.\n\n"
                f"Login here: {FRONTEND_URL}/login\n"
            )
        )

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_APP_PASSWORD)
            server.send_message(message)
    except Exception:
        # Non-blocking: registration should still succeed even if email fails.
        pass


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
):
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload is invalid.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


@router.post("/register")
def register_user(payload: RegisterRequest, background_tasks: BackgroundTasks):
    name = payload.name.strip()
    email = normalize_email(payload.email)

    if not name:
        raise HTTPException(status_code=400, detail="Name is required.")

    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        raise HTTPException(status_code=400, detail="Enter a valid email address.")

    if not password_is_valid(payload.password):
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters and include uppercase, lowercase, and a number.",
        )

    existing_user = users.find_one({"email": email})
    if existing_user:
        raise HTTPException(status_code=409, detail="An account with this email already exists.")

    password_hash = bcrypt.hashpw(payload.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    try:
        result = users.insert_one(
            {
                "name": name,
                "email": email,
                "password_hash": password_hash,
                "provider": "local",
                "created_at": datetime.utcnow(),
            }
        )
    except DuplicateKeyError as exc:
        raise HTTPException(status_code=409, detail="This email is already registered.") from exc

    created_user = users.find_one({"_id": result.inserted_id})
    background_tasks.add_task(send_welcome_email, name, email)

    token = create_token(created_user)
    return {
        "status": "success",
        "message": "Registration successful.",
        "token": token,
        "user": serialize_user(created_user),
    }


@router.post("/login")
def login_user(payload: LoginRequest):
    email = normalize_email(payload.email)
    user = users.find_one({"email": email})

    if not user or not user.get("password_hash"):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    password_ok = bcrypt.checkpw(payload.password.encode("utf-8"), user["password_hash"].encode("utf-8"))
    if not password_ok:
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    token = create_token(user)
    return {
        "status": "success",
        "message": "Login successful.",
        "token": token,
        "user": serialize_user(user),
    }


@router.post("/google")
def google_login(payload: GoogleRequest):
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=400, detail="Google login is not configured.")

    try:
        id_info = id_token.verify_oauth2_token(
            payload.credential,
            google_requests.Request(),
            GOOGLE_CLIENT_ID,
        )
    except ValueError as exc:
        raise HTTPException(status_code=401, detail="Google credential verification failed.") from exc

    email = normalize_email(id_info.get("email", ""))
    if not email:
        raise HTTPException(status_code=400, detail="Google account email is required.")

    user = users.find_one({"email": email})

    if not user:
        result = users.insert_one(
            {
                "name": id_info.get("name") or email.split("@")[0],
                "email": email,
                "password_hash": "",
                "provider": "google",
                "google_id": id_info.get("sub"),
                "created_at": datetime.utcnow(),
            }
        )
        user = users.find_one({"_id": result.inserted_id})
    else:
        updates = {}
        if not user.get("google_id"):
            updates["google_id"] = id_info.get("sub")
        if user.get("provider") != "google":
            updates["provider"] = "google"
        if updates:
            users.update_one({"_id": user["_id"]}, {"$set": updates})
            user = users.find_one({"_id": user["_id"]})

    token = create_token(user)
    return {
        "status": "success",
        "message": "Google login successful.",
        "token": token,
        "user": serialize_user(user),
    }


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "status": "success",
        "user": serialize_user(current_user),
    }
