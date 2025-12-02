# 🌍 TripAI - Agentic AI Travel Planner

> **An intelligent travel planning system powered by specialized AI agents that create personalized itineraries based on natural language input.**

Instead of manually searching for flights, hotels, and tourist attractions, TripAI acts as your AI travel concierge. Simply describe your dream trip, and our multi-agent system will craft the perfect itinerary tailored to your preferences and budget.

## ✨ Features

- **🤖 Multi-Agent AI System**: Specialized agents for NLP, itinerary planning, route optimization, and budget validation
- **💬 Conversational Interface**: Natural language trip planning - just describe your ideal vacation
- **💰 Smart Budget Management**: Automatic budget breakdown and cost optimization
- **🎯 Personalized Recommendations**: Learns from your preferences for better future suggestions
- **📅 Day-wise Itineraries**: Detailed timeline with activities, locations, costs, and tips
- **🔄 Preference Learning**: Remembers your tastes (dietary, activities, budget) for future trips
- **🌐 Real-time API Integration**: Google Places API for attractions, OpenAI GPT-4 for intelligence

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (React)                     │
│  Chat Interface → Itinerary Display → Dashboard             │
└──────────────────┬──────────────────────────────────────────┘
                   │ REST API
┌──────────────────▼──────────────────────────────────────────┐
│                    Backend (Node.js + Express)               │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │          Agent Orchestrator                        │    │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐ ┌────────┐│    │
│  │  │   NLP   │→ │Itinerary│→ │  Budget │→│Results ││    │
│  │  │  Agent  │  │  Agent  │  │  Agent  │ │        ││    │
│  │  └────┬────┘  └────┬────┘  └────┬────┘ └────────┘│    │
│  └───────┼────────────┼────────────┼──────────────────┘    │
│          │            │            │                        │
│   ┌──────▼─────┐  ┌──▼────────┐  ┌▼─────────┐            │
│   │ OpenAI LLM │  │ Travel API│  │ MongoDB  │            │
│   │   Service  │  │  Service  │  │ Database │            │
│   └────────────┘  └───────────┘  └──────────┘            │
└──────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **MongoDB** (local or MongoDB Atlas)
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- **Google Places API Key** (Optional, [Get one here](https://developers.google.com/maps/documentation/places/web-service/get-api-key))

### Installation

1. **Clone the repository**
```bash
cd "C:\Users\Somashekar M\OneDrive\Desktop\Agentic- Tripai"
```

2. **Backend Setup**
```bash
cd backend
npm install

# Create .env file
copy .env.example .env
```

3. **Configure Environment Variables**

Edit `backend/.env` and add your API keys:
```env
PORT=5000
MONGODB_URI=mongodb://localhost:27017/tripai
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_PLACES_API_KEY=your_google_places_api_key_here
FRONTEND_URL=http://localhost:5173
```

4. **Frontend Setup**
```bash
cd ../frontend
npm install
```

5. **Start Development Servers**

Terminal 1 (Backend):
```bash
cd backend
npm run dev
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

6. **Open the Application**

Navigate to `http://localhost:5173` in your browser

## 📖 Usage

### Planning a Trip

Simply type your trip request in natural language:

```
"3-day weekend trip to Goa, under ₹15,000, I prefer beaches and good veg food."
```

```
"5-day honeymoon in Kerala, budget ₹50,000, romantic places and backwaters"
```

```
"Week-long trek in Himachal Pradesh, ₹20,000, adventure and mountain views"
```

### What You Get

- **Day-wise itinerary** with timed activities
- **Budget breakdown** (accommodation, food, activities, transport)
- **Cost estimates** for each activity
- **Location details** and recommendations
- **Insider tips** for better experiences
- **Savings suggestions** if over budget

## 🧠 AI Agents Explained

### 1. **NLP Agent**
- Parses natural language queries
- Extracts destination, duration, budget, preferences
- Handles diverse input formats
- Fallback regex-based parsing for reliability

### 2. **Itinerary Agent**
- Fetches places from Google Places API
- Generates day-wise activity schedules
- Considers user preferences (dietary, activities)
- Creates realistic timings and durations

### 3. **Budget Agent**
- Validates total costs against budget
- Provides detailed breakdown
- Suggests adjustments if over budget
- Identifies savings opportunities

### 4. **Orchestrator**
- Coordinates all agents in sequence
- Manages data flow between agents
- Handles errors and retries
- Updates user preferences for learning

## 🛠️ Tech Stack

### Backend
- **Node.js** + **Express** - REST API server
- **MongoDB** + **Mongoose** - Data persistence
- **OpenAI API** (GPT-4o-mini) - AI intelligence
- **Google Places API** - Tourist attractions
- **Axios** - HTTP requests

### Frontend
- **React** 18 - UI framework
- **React Router** - Navigation
- **Vite** - Build tool
- **Vanilla CSS** - Premium design system

### Design Features
- Dark mode with vibrant gradients
- Glassmorphism effects
- Smooth micro-animations
- Responsive mobile-first design
- Google Fonts (Inter, Outfit)

## 📁 Project Structure

```
TripAI/
├── backend/
│   ├── agents/
│   │   ├── orchestrator.js      # Main coordinator
│   │   ├── nlpAgent.js          # Query parser
│   │   ├── itineraryAgent.js    # Itinerary creator
│   │   └── budgetAgent.js       # Budget validator
│   ├── models/
│   │   ├── User.js              # User preferences
│   │   └── Trip.js              # Trip data
│   ├── routes/
│   │   ├── planRoutes.js        # Trip planning API
│   │   └── userRoutes.js        # User management API
│   ├── services/
│   │   ├── llmService.js        # OpenAI integration
│   │   └── travelAPI.js         # Google Places integration
│   ├── server.js                # Express server
│   └── package.json
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.jsx      # Conversational UI
│   │   │   └── ItineraryDisplay.jsx   # Trip visualization
│   │   ├── pages/
│   │   │   ├── Home.jsx               # Landing + chat
│   │   │   └── Dashboard.jsx          # User dashboard
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css            # Design system
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
└── README.md
```

## 🔧 API Endpoints

### Trip Planning
- `POST /api/plan/create` - Create new trip plan
- `GET /api/plan/:id` - Get trip details
- `PATCH /api/plan/:id/feedback` - Submit feedback
- `POST /api/plan/:id/refine` - Refine existing plan

### User Management
- `GET /api/user/preferences` - Get user preferences
- `PUT /api/user/preferences` - Update preferences
- `GET /api/user/trips` - Get trip history

### Health Check
- `GET /api/health` - Server health status

## 🎨 UI Highlights

- **Animated Hero Section** with floating gradient orbs
- **Conversational Chat** with typing indicators
- **Timeline Itinerary** with color-coded activities
- **Budget Visualization** with breakdown charts
- **Responsive Design** for mobile/tablet/desktop
- **Premium Aesthetics** with modern gradients and glassmorphism

## 🔑 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `PORT` | Backend server port | No (default: 5000) |
| `MONGODB_URI` | MongoDB connection string | Yes |
| `OPENAI_API_KEY` | OpenAI API key for LLM | Yes |
| `GOOGLE_PLACES_API_KEY` | Google Places API key | No* |
| `FRONTEND_URL` | Frontend URL for CORS | No (default: localhost:5173) |

*Falls back to mock data if not provided

## 🚧 Future Enhancements

- [ ] Real flight and hotel API integration
- [ ] User authentication (JWT)
- [ ] Social sharing of itineraries
- [ ] Export to PDF/Calendar
- [ ] Multi-language support
- [ ] Collaborative trip planning
- [ ] Weather integration
- [ ] Real-time pricing updates

## 📝 Notes

- **Mock Data**: Flight and hotel data currently uses mock responses. Integrate with Amadeus or Booking.com APIs for production.
- **Free Tier**: Google Places API has a free tier (but requires billing enabled). Monitor usage to avoid charges.
- **OpenAI Costs**: GPT-4o-mini is cost-effective (~$0.15/1M tokens). Adjust model in `llmService.js` if needed.
- **Database**: MongoDB connection falls back gracefully for development. Ensure MongoDB is running for persistence.

## 🤝 Contributing

This is a demonstration project. Feel free to fork, enhance, and use as a learning resource!

## 📄 License

MIT License - Feel free to use this project for learning and personal use.

---

**Built with ❤️ using OpenAI GPT-4, Google Places API, React, and Node.js**
