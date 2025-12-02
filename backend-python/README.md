# TripAI Python Backend 🐍

Python-based backend for the Agentic AI Travel Planner with FastAPI and async AI agents.

## 🚀 Quick Start

### 1. Create Virtual Environment
```powershell
cd backend-python
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Configure Environment
```powershell
copy .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 4. Run the Server
```powershell
python main.py
```

The server will start on **http://localhost:5001**

## 📂 Structure

```
backend-python/
├── agents/
│   ├── nlp_agent.py          # Natural language parsing
│   ├── itinerary_agent.py    # Trip planning
│   ├── budget_agent.py       # Budget validation
│   └── orchestrator.py       # Agent coordinator
├── models/
│   ├── user.py               # User Pydantic models
│   └── trip.py               # Trip Pydantic models
├── services/
│   ├── llm_service.py        # OpenAI integration
│   └── travel_api.py         # Google Places API
├── main.py                   # FastAPI application
├── requirements.txt
└── .env
```

## 🔑 Features

- ✅ **FastAPI** - Modern Python web framework
- ✅ **Async/Await** - Non-blocking AI agent operations
- ✅ **Pydantic Models** - Type-safe data validation
- ✅ **OpenAI Python SDK** - Native GPT-4 integration
- ✅ **Auto-generated API Docs** - Available at `/docs`

## 📖 API Endpoints

### Health Check
```
GET /api/health
```

### Create Travel Plan
```
POST /api/plan/create
Body: {
  "query": "3-day trip to Goa under ₹15,000",
  "userId": "demo-user-123"
}
```

## 🧪 Testing

Visit **http://localhost:5001/docs** for interactive API documentation (Swagger UI).

## 🔄 Integration with Frontend

To use the Python backend with the existing frontend:

1. Stop the Node.js backend
2. Start the Python backend on port 5001
3. Update frontend proxy in `vite.config.js`:
   ```javascript
   proxy: {
     '/api': {
       target: 'http://localhost:5001'
     }
   }
   ```
4. Restart frontend

Or keep both running on different ports for testing.

## 🎯 Benefits Over Node.js Version

- Native Python for ML/AI workflows
- Better LangChain integration (future)
- Type safety with Pydantic
- Async performance with FastAPI
- Auto-generated API documentation
- Easier to add custom ML models

## 📝 Requirements

- Python 3.8+
- OpenAI API key
- (Optional) Google Places API key
