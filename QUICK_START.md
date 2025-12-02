# 🚀 TripAI - Quick Start Guide

## Current Status: ✅ RUNNING

Both backend and frontend are currently running and ready to use!

## 🌐 Access URLs

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:5173 | Main application interface |
| **Backend API** | http://localhost:5001 | REST API server |
| **API Docs** | http://localhost:5001/docs | Interactive API documentation |
| **Health Check** | http://localhost:5001/api/health | Backend health status |

## 🏃 How to Start Servers (If Stopped)

### Terminal 1 - Backend
```powershell
cd "d:\Agentic- Tripai\backend-python"
python main.py
```

### Terminal 2 - Frontend
```powershell
cd "d:\Agentic- Tripai\frontend"
npm run dev
```

## 🛑 How to Stop Servers

Press `Ctrl+C` in each terminal window

## 🎯 Quick Test

1. Open http://localhost:5173 in your browser
2. Enter a trip query: "3-day trip to Goa under ₹15,000"
3. Wait for the AI to generate your itinerary

## 🔧 Tech Stack

- **Backend**: Python 3.12.5 + FastAPI + Gemini AI
- **Frontend**: React 18 + Vite 5
- **Database**: MongoDB Atlas
- **APIs**: Gemini AI, MapMyIndia

## 📂 Project Structure

```
d:\Agentic- Tripai\
├── backend-python/          # Python FastAPI backend
│   ├── main.py             # Server entry point
│   ├── .env                # Environment variables
│   ├── agents/             # AI agents
│   ├── routes/             # API routes
│   └── services/           # LLM & API services
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # UI components
│   │   └── pages/          # Page components
│   └── vite.config.js      # Vite configuration
└── SERVER_STATUS.md        # Detailed server info
```

## 💡 Tips

- Both servers support hot-reload (changes are reflected automatically)
- Backend API docs at http://localhost:5001/docs are interactive
- Check `backend-python/logs/` for detailed logs
- Environment variables are in `backend-python/.env`

## 🐛 Troubleshooting

**Backend not starting?**
- Check if port 5001 is available
- Verify `.env` file has all required keys
- Check Python version: `python --version` (need 3.8+)

**Frontend not starting?**
- Check if port 5173 is available
- Run `npm install` in frontend directory
- Check Node version: `node --version` (need 18+)

**API calls failing?**
- Check CORS settings in backend `.env`
- Verify proxy settings in `vite.config.js`
- Check backend is running on port 5001

---

**Last Updated**: December 2, 2025
