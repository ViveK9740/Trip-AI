from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from bson import ObjectId


class PyObjectId(str):
    """Custom ObjectId type for Pydantic"""
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


class PreferencesModel(BaseModel):
    """User preferences sub-document"""
    dietary: List[str] = Field(default_factory=list)
    activities: List[str] = Field(default_factory=list)
    budget_range: dict = Field(default_factory=lambda: {"min": 0, "max": 50000})
    travel_style: str = "moderate"
    accommodation_type: List[str] = Field(default_factory=lambda: ["hotel"])


class LearningDataModel(BaseModel):
    """Learning metadata"""
    total_trips: int = 0
    favorite_destinations: List[str] = Field(default_factory=list)
    average_budget: float = 0.0
    last_updated: datetime = Field(default_factory=datetime.now)


class UserModel(BaseModel):
    """User model with preferences and learning data"""
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    name: str
    email: str
    preferences: PreferencesModel = Field(default_factory=PreferencesModel)
    trip_history: List[PyObjectId] = Field(default_factory=list)
    learning_data: LearningDataModel = Field(default_factory=LearningDataModel)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def update_learning_data(self, trip):
        """Update learning data based on new trip"""
        self.learning_data.total_trips += 1
        
        if trip.destination not in self.learning_data.favorite_destinations:
            self.learning_data.favorite_destinations.append(trip.destination)
        
        # Recalculate average budget
        total_budget = (
            self.learning_data.average_budget * (self.learning_data.total_trips - 1) 
            + trip.budget
        )
        self.learning_data.average_budget = total_budget / self.learning_data.total_trips
        self.learning_data.last_updated = datetime.now()


class UserInDB(UserModel):
    """User model for database operations"""
    pass
