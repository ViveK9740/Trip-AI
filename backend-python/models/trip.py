from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime
from bson import ObjectId
from .user import PyObjectId


class LocationModel(BaseModel):
    """Location information"""
    name: str
    address: Optional[str] = None
    coordinates: Optional[Dict[str, float]] = None


class ActivityModel(BaseModel):
    """Single activity in itinerary"""
    time: str
    type: str  # sightseeing, food, activity, travel, rest
    name: str
    description: Optional[str] = ""
    location: Optional[LocationModel] = None
    estimated_cost: float = 0.0
    duration: str = "2 hours"
    tips: Optional[str] = ""


class DayPlanModel(BaseModel):
    """Single day in itinerary"""
    day: int
    date: Optional[datetime] = None
    activities: List[ActivityModel] = Field(default_factory=list)
    total_cost: float = 0.0
    summary: str = ""


class DurationModel(BaseModel):
    """Trip duration"""
    days: int
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class PreferencesModel(BaseModel):
    """Trip preferences"""
    dietary: List[str] = Field(default_factory=list)
    activities: List[str] = Field(default_factory=list)


class BudgetBreakdownModel(BaseModel):
    """Budget breakdown"""
    accommodation: float = 0.0
    food: float = 0.0
    activities: float = 0.0
    transportation: float = 0.0
    miscellaneous: float = 0.0
    total: float = 0.0


class FeedbackModel(BaseModel):
    """User feedback"""
    rating: Optional[int] = None
    comments: Optional[str] = None
    helpful_activities: List[str] = Field(default_factory=list)
    skipped_activities: List[str] = Field(default_factory=list)


class AgentMetadataModel(BaseModel):
    """Agent processing metadata"""
    processing_time: float = 0.0
    agents_used: List[str] = Field(default_factory=list)
    iterations: int = 1


class TripModel(BaseModel):
    """Trip model with complete itinerary"""
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    user_id: Optional[PyObjectId] = None
    user_query: str
    destination: str
    duration: DurationModel
    budget: float
    preferences: PreferencesModel
    itinerary: List[DayPlanModel] = Field(default_factory=list)
    budget_breakdown: BudgetBreakdownModel = Field(default_factory=BudgetBreakdownModel)
    status: str = "draft"  # draft, confirmed, completed, cancelled
    feedback: Optional[FeedbackModel] = None
    agent_metadata: AgentMetadataModel = Field(default_factory=AgentMetadataModel)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class TripInDB(TripModel):
    """Trip model for database operations"""
    pass


class TripCreate(BaseModel):
    """Trip creation request"""
    query: str
    user_id: Optional[str] = "demo-user-123"


class TripResponse(BaseModel):
    """Trip creation response"""
    success: bool
    trip_id: str
    destination: str
    duration: DurationModel
    budget: float
    itinerary: List[DayPlanModel]
    budget_validation: Dict[str, Any]
    processing_time: float
    message: str
