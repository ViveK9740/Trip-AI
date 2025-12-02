from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional
from database.db import get_users_collection
from utils.auth import hash_password, verify_password, create_access_token, verify_token
from models.schemas import UserModel, UserResponse
from bson import ObjectId

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
security = HTTPBearer()

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    user: UserResponse
    token: str

@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(request: SignupRequest):
    """Register a new user"""
    users = get_users_collection()
    
    # Check if user already exists
    existing_user = users.find_one({"email": request.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    password_hash = hash_password(request.password)
    
    # Create user document
    user_doc = UserModel(
        email=request.email,
        password_hash=password_hash,
        name=request.name
    )
    
    # Insert into database
    result = users.insert_one(user_doc.model_dump(by_alias=True))
    user_id = str(result.inserted_id)
    
    # Create JWT token
    token = create_access_token({"sub": user_id})
    
    # Return user and token
    user_response = UserResponse(
        id=user_id,
        email=user_doc.email,
        name=user_doc.name,
        created_at=user_doc.created_at
    )
    
    return AuthResponse(user=user_response, token=token)

@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    """Login user"""
    users = get_users_collection()
    
    # Find user by email
    user = users.find_one({"email": request.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(request.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create JWT token
    token = create_access_token({"sub": str(user["_id"])})
    
    # Return user and token
    user_response = UserResponse(
        id=str(user["_id"]),
        email=user["email"],
        name=user["name"],
        created_at=user["created_at"]
    )
    
    return AuthResponse(user=user_response, token=token)

@router.get("/me", response_model=UserResponse)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user from token"""
    token = credentials.credentials
    user_id = verify_token(token)
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    users = get_users_collection()
    user = users.find_one({"_id": ObjectId(user_id)})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=str(user["_id"]),
        email=user["email"],
        name=user["name"],
        created_at=user["created_at"]
    )

# Helper function to get current user (for use in other routes)
async def get_user_from_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Get user from token - for use as dependency in other routes"""
    token = credentials.credentials
    user_id = verify_token(token)
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    users = get_users_collection()
    user = users.find_one({"_id": ObjectId(user_id)})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user
