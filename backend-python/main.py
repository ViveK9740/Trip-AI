from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from dotenv import load_dotenv
from agents.orchestrator import orchestrator
from routes import auth, trips

load_dotenv()

app = FastAPI(
    title="TripAI Python Backend",
    description="Agentic AI Travel Planner with Python agents",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:5173")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(trips.router)


# Request/Response Models
class PlanRequest(BaseModel):
    query: str
    userId: str = "demo-user-123"
    preferences: dict = {}
    origin: str = None
    is_round_trip: bool = False


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    python_version: str


# Routes
@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    import sys
    from datetime import datetime
    
    return HealthResponse(
        status="ok",
        timestamp=datetime.now().isoformat(),
        python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )


@app.post("/api/plan/create")
async def create_plan(request: PlanRequest):
    """Create a new travel plan from user query"""
    try:
        if not request.query:
            raise HTTPException(status_code=400, detail="Query is required")
        
        # Add origin and round trip to preferences if present
        if request.origin:
            request.preferences['origin'] = request.origin
        request.preferences['is_round_trip'] = request.is_round_trip

        # Create travel plan using agent orchestrator
        result = await orchestrator.create_travel_plan(
            request.query, 
            request.userId,
            request.preferences
        )
        
        return result
        
    except Exception as e:
        print(f"Plan creation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "TripAI Python Backend",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }


@app.get("/api/test-db")
async def test_db():
    """Test MongoDB connection"""
    try:
        from database.db import get_users_collection
        users = get_users_collection()
        count = users.count_documents({})
        return {"status": "connected", "user_count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    print(f"🚀 TripAI Python Backend starting on port {port}...")
    print(f"📊 Health check: http://localhost:{port}/api/health")
    print(f"📖 API docs: http://localhost:{port}/docs")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # Disable auto-reload to prevent crashes
        log_level="info"
    )
