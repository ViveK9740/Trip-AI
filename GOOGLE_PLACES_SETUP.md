# 🗺️ Google Places API Setup Guide

## Get Your Free API Key

Google Places API has a **FREE tier** with $200 monthly credit (enough for ~40,000 place searches).

### Step 1: Go to Google Cloud Console
Visit: https://console.cloud.google.com/

### Step 2: Create a New Project
1. Click "Select a project" → "New Project"
2. Name it "TripAI" or similar
3. Click "Create"

### Step 3: Enable Places API
1. Go to "APIs & Services" → "Library"
2. Search for "**Places API**"
3. Click on it and press "**Enable**"

### Step 4: Create API Key
1. Go to "APIs & Services" → "Credentials"
2. Click "**Create Credentials**" → "API Key"
3. Copy your API key (starts with `AIza...`)

### Step 5: (Optional but Recommended) Restrict the Key
1. Click on your API key to edit it
2. Under "API restrictions" select "Restrict key"
3. Choose "Places API" from the list
4. Save

### Step 6: Enable Billing (Required for Free Tier)
1. Go to "Billing" in the console
2. Set up billing account (won't be charged unless you exceed $200/month)
3. Credit card required but you get $200 free credit monthly

## Add to Your Project

### For Python Backend:
Edit `backend-python/.env`:
```env
GOOGLE_PLACES_API_KEY=AIzaSyXxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### For Node.js Backend (Optional):
Edit `backend/.env`:
```env
GOOGLE_PLACES_API_KEY=AIzaSyXxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Test It!

Start the Python backend:
```powershell
cd backend-python
.\venv\Scripts\activate
python main.py
```

Try a query:
```
"3-day trip to Goa, beaches and veg food"
```

You should now see **real place names** like:
- ✅ Baga Beach (with actual address and ratings)
- ✅ Fort Aguada, Candolim
- ✅ Actual restaurant names with ratings
- ✅ Real geo-coordinates

## Without API Key

If you don't add a key, the system will use enhanced mock data - still works but with generic place names.

## Cost Estimate

- **Place Nearby Search**: $0.032 per request
- **Geocoding**: $0.005 per request
- **Monthly Free Credit**: $200
- **Typical Usage**: ~3-5 requests per trip plan
- **Estimated trips per month**: ~1,000-2,000 trips FREE

## Troubleshooting

If you see errors:
1. Make sure billing is enabled (even for free tier)
2. Wait 1-2 minutes after enabling the API
3. Check API key is correctly copied
4. Verify "Places API" is enabled (not "Places API (New)")
