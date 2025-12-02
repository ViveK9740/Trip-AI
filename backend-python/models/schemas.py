from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId

class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        return core_schema.union_schema([
            core_schema.is_instance_schema(ObjectId),
            core_schema.chain_schema([
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(cls.validate),
            ])
        ])

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(ObjectId(v))

class UserModel(BaseModel):
    email: EmailStr
    password_hash: str
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }
    
    def dict(self, **kwargs):
        """Override dict for backward compatibility"""
        return super().model_dump(**kwargs)

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    created_at: datetime

class TripModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    destination: str
    start_date: Optional[str]
    end_date: Optional[str]
    days: int
    budget: Optional[float]
    itinerary_data: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

class TripResponse(BaseModel):
    id: str
    destination: str
    start_date: Optional[str]
    end_date: Optional[str]
    days: int
    budget: Optional[float]
    created_at: datetime

class TripDetailResponse(TripResponse):
    itinerary_data: Dict[str, Any]
