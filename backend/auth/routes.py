import redis
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from backend.auth.jwt_handler import create_access_token, create_refresh_token, verify_token
from backend.database import get_user, verify_password, create_user
from backend.config import REDIS_URL # Import REDIS_URL for Redis connection

# Connect to Redis for the logout blacklist
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

router = APIRouter(prefix="/auth", tags=["Authentication"])

# --- Pydantic Models for Input Validation ---
class AuthRequest(BaseModel):
    username: str
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

# --- Endpoints ---
@router.post("/register")
def register(body: AuthRequest):
    # Check if user already exists
    existing_user = get_user(body.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Save to database
    create_user(body.username, body.password)
    return {"message": "User registered successfully"}

@router.post("/login")
def login(body: AuthRequest):
    user = get_user(body.username)
    if not user or not verify_password(body.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": create_access_token(body.username),
        "refresh_token": create_refresh_token(body.username),
        "token_type": "bearer"
    }

@router.post("/refresh")
def refresh(body: RefreshRequest):
    username = verify_token(body.refresh_token, expected_type="refresh")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    
    return {
        "access_token": create_access_token(username),
        "token_type": "bearer"
    }

@router.post("/logout")
def logout(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid Authorization header")
    
    # Extract the token
    token = authorization.split(" ")[1]
    
    # Verify the token before blacklisting it
    if not verify_token(token, expected_type="access"):
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    # Add token to Redis blacklist for 1 hour (3600 seconds)
    redis_client.setex(f"blacklist:{token}", 3600, "true")
    
    return {"message": "Logged out successfully"}