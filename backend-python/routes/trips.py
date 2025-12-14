from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from database.db import get_trips_collection
from routes.auth import get_user_from_token
from models.schemas import TripModel, TripResponse, TripDetailResponse
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/api/trips", tags=["Trips"])
security = HTTPBearer()

class SaveTripRequest(BaseModel):
    destination: str
    start_date: Optional[str]
    end_date: Optional[str]
    days: int
    budget: Optional[float]
    itinerary_data: Dict[str, Any]

@router.post("/", response_model=TripDetailResponse, status_code=status.HTTP_201_CREATED)
async def save_trip(
    request: SaveTripRequest,
    user: dict = Depends(get_user_from_token)
):
    """Save a new trip for the authenticated user"""
    trips = get_trips_collection()
    
    # Create trip document without _id field - let MongoDB auto-generate it
    trip_dict = {
        "user_id": str(user["_id"]),
        "destination": request.destination,
        "start_date": request.start_date,
        "end_date": request.end_date,
        "days": request.days,
        "budget": request.budget,
        "itinerary_data": request.itinerary_data,
        "created_at": datetime.utcnow()
    }
    
    result = trips.insert_one(trip_dict)
    trip_id = str(result.inserted_id)
    
    # Create TripModel for response
    trip_doc = TripModel(
        id=trip_id,
        user_id=trip_dict["user_id"],
        destination=trip_dict["destination"],
        start_date=trip_dict["start_date"],
        end_date=trip_dict["end_date"],
        days=trip_dict["days"],
        budget=trip_dict["budget"],
        itinerary_data=trip_dict["itinerary_data"],
        created_at=trip_dict["created_at"]
    )
    
    return TripDetailResponse(
        id=trip_id,
        destination=trip_doc.destination,
        start_date=trip_doc.start_date,
        end_date=trip_doc.end_date,
        days=trip_doc.days,
        budget=trip_doc.budget,
        itinerary_data=trip_doc.itinerary_data,
        created_at=trip_doc.created_at
    )

@router.get("/", response_model=List[TripResponse])
async def get_user_trips(user: dict = Depends(get_user_from_token)):
    """Get all trips for the authenticated user"""
    trips = get_trips_collection()
    
    user_trips = list(trips.find({"user_id": str(user["_id"])}).sort("created_at", -1))
    
    return [
        TripResponse(
            id=str(trip["_id"]),
            destination=trip["destination"],
            start_date=trip.get("start_date"),
            end_date=trip.get("end_date"),
            days=trip["days"],
            budget=trip.get("budget"),
            created_at=trip["created_at"]
        )
        for trip in user_trips
    ]

@router.get("/{trip_id}", response_model=TripDetailResponse)
async def get_trip(trip_id: str, user: dict = Depends(get_user_from_token)):
    """Get a specific trip by ID"""
    trips = get_trips_collection()
    
    try:
        trip = trips.find_one({"_id": ObjectId(trip_id), "user_id": str(user["_id"])})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid trip ID"
        )
    
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found"
        )
    
    return TripDetailResponse(
        id=str(trip["_id"]),
        destination=trip["destination"],
        start_date=trip.get("start_date"),
        end_date=trip.get("end_date"),
        days=trip["days"],
        budget=trip.get("budget"),
        itinerary_data=trip["itinerary_data"],
        created_at=trip["created_at"]
    )

@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trip(trip_id: str, user: dict = Depends(get_user_from_token)):
    """Delete a trip"""
    trips = get_trips_collection()
    
    try:
        result = trips.delete_one({"_id": ObjectId(trip_id), "user_id": str(user["_id"])})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid trip ID"
        )
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found"
        )
    
    return None
