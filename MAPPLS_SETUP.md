# 🗺️ MapMyIndia (Mappls) API Setup Guide

## Why Mappls?
- ✅ **Better for India** - Superior coverage of Indian locations
- ✅ **Easier Access** - Simple signup, instant API keys
- ✅ **Free Tier** - Generous free usage limits
- ✅ **Includes** - Places, geocoding, routing, maps

## Get Your Free API Key

### Step 1: Sign Up
Visit: https://about.mappls.com/api/

### Step 2: Register
1. Click "**Sign Up**" or "**Get Started**"
2. Fill in your details
3. Verify your email

### Step 3: Get API Keys
1. Login to your dashboard
2. Go to "**API Keys**" or "**Credentials**"
3. You'll get two keys:
   - **REST API Key** (for places/geocoding)
   - **Map SDK Key** (optional, for maps)

### Step 4: Copy Your Keys
```
REST API Key: e.g., abc123xyz456...
Client ID: (if provided)
Client Secret: (if provided)
```

## Add to Your Project

Edit `backend-python/.env`:
```env
MAPPLS_API_KEY=your_rest_api_key_here
MAPPLS_CLIENT_ID=your_client_id_here (optional)
MAPPLS_CLIENT_SECRET=your_client_secret_here (optional)
```

## Test It!

Start Python backend:
```powershell
cd backend-python
.\venv\Scripts\activate
python main.py
```

Try: "3-day trip to Goa, beaches and veg food"

You'll get **real Indian places**:
- ✅ Baga Beach, North Goa
- ✅ Fort Aguada, Candolim
- ✅ Actual restaurants with Indian addresses
- ✅ Accurate geo-coordinates for India

## API Features

**Mappls provides:**
- 🔍 Place Search (POI)
- 📍 Geocoding (address → coordinates)
- 🗺️ Reverse Geocoding (coordinates → address)
- 🛣️ Routing & Directions
- 🏨 Hotels, Restaurants, Attractions

## Free Tier Limits

- **Free** for development/testing
- Generous daily limits
- No credit card required initially
- Enterprise plans available if needed

## Documentation

- API Docs: https://www.mappls.com/api/
- Place Search: https://www.mappls.com/api/advanced-maps/doc/place-search-api
- Geocoding: https://www.mappls.com/api/advanced-maps/doc/geocoding-api

## Troubleshooting

If you see errors:
1. Verify API key is correct
2. Check if API is enabled in dashboard
3. Ensure you're using the **REST API Key** (not Map SDK Key)
4. May need to wait a few minutes after signup
