import os
import httpx
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from utils.logger import log_data

load_dotenv()


class TravelAPIService:
    """
    Travel API Service
    Integrates with MapMyIndia (Mappls) API for Indian location data
    """
    
    def __init__(self):
        self.mappls_client_id = os.getenv("MAPPLS_CLIENT_ID")
        self.mappls_client_secret = os.getenv("MAPPLS_CLIENT_SECRET")
        self.mappls_base_url = "https://atlas.mappls.com/api/places"
        self.mappls_token_url = "https://outpost.mappls.com/api/security/oauth/token"
        self.access_token = None
        self.token_expiry = None
        
        if self.mappls_client_id and self.mappls_client_secret:
            print("✅ Mappls API initialized")
        else:
            print("⚠️  No Mappls credentials, using mock data")
    
    async def _get_access_token(self) -> str:
        """Generate or return cached Mappls access token"""
        from datetime import datetime, timedelta
        
        # Return cached token if still valid
        if self.access_token and self.token_expiry and datetime.now() < self.token_expiry:
            return self.access_token
        
        # Generate new token
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.mappls_token_url,
                    data={
                        "grant_type": "client_credentials",
                        "client_id": self.mappls_client_id,
                        "client_secret": self.mappls_client_secret
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    token_data = response.json()
                    self.access_token = token_data.get("access_token")
                    # Token valid for 24 hours, cache for 23 to be safe
                    self.token_expiry = datetime.now() + timedelta(hours=23)
                    print(f"🔑 Mappls access token generated")
                    return self.access_token
                else:
                    print(f"⚠️  Token generation failed: {response.status_code}")
                    return None
        except Exception as e:
            print(f"❌ Token generation error: {e}")
            return None
    
    async def search_hotels(
        self, 
        destination: str, 
        budget_range: str = "mid_range"
    ) -> List[Dict[str, Any]]:
        """Search for hotels using Mappls API"""
        # Map budget range to keywords
        keywords = {
            "budget": "cheap hotel",
            "mid_range": "hotel",
            "luxury": "luxury hotel 5 star"
        }
        keyword = keywords.get(budget_range, "hotel")
        
        return await self.search_places(destination, keyword)



    async def search_places(
        self, 
        destination: str,
        category: str = "tourist attraction"
    ) -> List[Dict[str, Any]]:
        """Search for places/attractions using Mappls API"""
        if not self.mappls_client_id or not self.mappls_client_secret:
            print(f"⚠️ Mappls API not configured, using mock data for {destination}")
            return self._get_mock_places(destination)
        
        try:
            print(f"🗺️  Fetching real {category} for {destination}...")
            
            # Get access token
            access_token = await self._get_access_token()
            if not access_token:
                print("❌ Failed to get Mappls access token, using mock data")
                return self._get_mock_places(destination)
            
            # Enhanced query for better results
            query_string = f"{destination} {category}" if category in ["tourist attraction", "monument", "temple", "fort"] else f"{category} near {destination}"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.mappls_base_url}/search/json",
                    params={
                        "query": query_string,
                        "region": "IND",
                        "location": destination,
                        "access_token": access_token
                    },
                    timeout=15.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    log_data(f"MAPPLS PLACES API RESPONSE for {destination} ({category})", data)
                    print(f"✅ Mappls Places API Response received")
                    places = self._parse_mappls_places(data, destination, is_restaurant=False)
                    log_data(f"PARSED PLACES for {destination} ({category})", places)
                    print(f"✅ Found {len(places)} real places ({category})")
                    if places:
                        print(f"🔍 First place: {places[0].get('name')}")
                    return places if places else self._get_mock_places(destination)
                elif response.status_code == 403:
                    print("❌ Mappls API returned 403 Forbidden - using mock data")
                    print("💡 Check your Mappls dashboard: https://apis.mappls.com/console/")
                    return self._get_mock_places(destination)
                else:
                    print(f"❌ Mappls API returned status code: {response.status_code}, using mock data")
                    return self._get_mock_places(destination)
                    
        except Exception as e:
            print(f"❌ Places search error: {e}, using mock data")
            return self._get_mock_places(destination)
    
    async def search_restaurants(
        self, 
        destination: str,
        dietary: str = "any"
    ) -> List[Dict[str, Any]]:
        """Search for restaurants using Mappls API"""
        if not self.mappls_client_id or not self.mappls_client_secret:
            print(f"⚠️ Mappls API not configured, using mock restaurants for {destination}")
            return self._get_mock_restaurants(destination)
        
        try:
            print(f"🍽️  Fetching real restaurants for {destination}...")
            
            # Get access token
            access_token = await self._get_access_token()
            if not access_token:
                print("❌ Failed to get Mappls access token, using mock data")
                return self._get_mock_restaurants(destination)
            
            keyword = "vegetarian restaurant" if dietary and "veg" in str(dietary).lower() else "restaurant"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.mappls_base_url}/search/json",
                    params={
                        "query": f"{keyword} in {destination}",
                        "region": "IND",
                        "access_token": access_token
                    },
                    timeout=10.0
                )
                if response.status_code == 200:
                    data = response.json()
                    log_data(f"MAPPLS RESTAURANTS API RESPONSE for {destination}", data)
                    print(f"✅ Mappls Restaurant API Response received")
                    restaurants = self._parse_mappls_places(data, destination, is_restaurant=True)
                    log_data(f"PARSED RESTAURANTS for {destination}", restaurants)
                    print(f"✅ Found {len(restaurants)} real restaurants")
                    if restaurants:
                        print(f"🔍 First restaurant: {restaurants[0].get('name')}")
                    return restaurants if restaurants else self._get_mock_restaurants(destination)
                elif response.status_code == 403:
                    print("❌ Mappls API returned 403 Forbidden - using mock data")
                    print("💡 Check your Mappls dashboard: https://apis.mappls.com/console/")
                    return self._get_mock_restaurants(destination)
                else:
                    print(f"❌ Mappls API returned status code: {response.status_code}, using mock data")
                    return self._get_mock_restaurants(destination)
                    
        except Exception as e:
            print(f"❌ Restaurant search error: {e}, using mock data")
            return self._get_mock_restaurants(destination)

    
    async def _geocode_destination(self, destination: str) -> Optional[Dict[str, float]]:
        """Geocode destination to get coordinates (deprecated - not used in current flow)"""
        try:
            access_token = await self._get_access_token()
            if not access_token:
                return None
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://atlas.mappls.com/api/places/geocode",
                    params={
                        "address": destination,
                        "access_token": access_token
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("copResults"):
                        result = data["copResults"][0]
                        return {
                            "lat": float(result.get("latitude", 0)),
                            "lng": float(result.get("longitude", 0))
                        }
        except Exception as e:
            print(f"Geocoding error: {e}")
        
        return None
    
    def _format_review_data(self, rating: float, total_reviews: int) -> dict:
        """Format review data with rating category"""
        return {
            "rating": rating,
            "total_reviews": total_reviews,
            "rating_category": self._get_rating_category(rating),
            "rating_stars": round(rating * 2) / 2  # Round to nearest 0.5
        }
    
    def _get_rating_category(self, rating: float) -> str:
        """Get rating category label"""
        if rating >= 4.5:
            return "Excellent"
        elif rating >= 4.0:
            return "Very Good"
        elif rating >= 3.5:
            return "Good"
        elif rating >= 3.0:
            return "Average"
        else:
            return "Below Average"
    
    def _parse_mappls_places(
        self, 
        data: Dict, 
        destination: str, 
        is_restaurant: bool = False
    ) -> List[Dict[str, Any]]:
        """Parse Mappls API response into our format with enhanced filtering"""
        places = []
        
        # Mappls returns different structures depending on the endpoint
        results = data.get("suggestedLocations", []) or data.get("results", [])
        
        print(f"🔍 Mappls returned {len(results)} total results for {destination}")
        
        # Increase limit for attractions, keep lower for restaurants
        max_results = 10 if is_restaurant else 25
        
        # Split destination into keywords for better matching
        dest_keywords = [word.lower() for word in destination.split() if len(word) > 2]
        
        for idx, place in enumerate(results[:max_results]):
            # Get place details
            address = place.get("placeAddress") or place.get("address", "")
            name = place.get("placeName") or place.get("name", "")
            place_type = place.get("type", "")
            
            # Very lenient filtering - accept if ANY destination keyword appears ANYWHERE
            # in the address or name, OR if it's from the search results (trust the API)
            destination_match = any(
                keyword in address.lower() or keyword in name.lower() 
                for keyword in dest_keywords
            )
            
            # Debug logging for first few results
            if idx < 3:
                print(f"  Result {idx+1}: '{name}' at '{address}' - Match: {destination_match}")
            
            # Accept all results from Mappls API since we searched for this destination
            # The API already filtered by destination, so we trust its results
            places.append({
                "name": name,
                "address": address,
                "rating": 4.0 + (hash(place.get("eLoc", "")) % 10) / 10,  # Mock rating
                "user_ratings_total": 500 + (hash(place.get("eLoc", "")) % 5000),
                "types": ["restaurant"] if is_restaurant else ["tourist_attraction"],
                "location": {
                    "lat": float(place.get("latitude", 0)) if place.get("latitude") else 0,
                    "lng": float(place.get("longitude", 0)) if place.get("longitude") else 0
                },
                "place_id": place.get("eLoc", ""),  # Mappls uses eLoc as unique ID
                "price_level": 2 if is_restaurant else None
            })
        
        print(f"✅ Parsed {len(places)} places from Mappls API")
        return places
    
    def _get_mock_places(self, destination: str) -> List[Dict[str, Any]]:
        """Enhanced mock places data with Indian destinations"""
        mock_places = {
            "goa": [
                {
                    "name": "Baga Beach",
                    "address": "Baga, North Goa, Goa 403516",
                    "rating": 4.5,
                    "user_ratings_total": 15420,
                    "types": ["beach", "tourist_attraction"],
                    "location": {"lat": 15.5559, "lng": 73.7516}
                },
                {
                    "name": "Fort Aguada",
                    "address": "Aguada Fort Road, Candolim, Goa 403515",
                    "rating": 4.3,
                    "user_ratings_total": 12340,
                    "types": ["historical", "fort", "tourist_attraction"],
                    "location": {"lat": 15.4909, "lng": 73.7730}
                },
                {
                    "name": "Dudhsagar Waterfalls",
                    "address": "Mollem National Park, Goa",
                    "rating": 4.7,
                    "user_ratings_total": 8920,
                    "types": ["nature", "waterfall", "tourist_attraction"],
                    "location": {"lat": 15.3144, "lng": 74.3144}
                },
                {
                    "name": "Basilica of Bom Jesus",
                    "address": "Old Goa Road, Bainguinim, Goa 403402",
                    "rating": 4.6,
                    "user_ratings_total": 11250,
                    "types": ["church", "historical", "unesco_heritage"],
                    "location": {"lat": 15.5007, "lng": 73.9114}
                },
                {
                    "name": "Anjuna Beach",
                    "address": "Anjuna, North Goa, Goa 403509",
                    "rating": 4.4,
                    "user_ratings_total": 9870,
                    "types": ["beach", "tourist_attraction"],
                    "location": {"lat": 15.5736, "lng": 73.7397}
                },
                {
                    "name": "Calangute Beach",
                    "address": "Calangute, North Goa, Goa 403516",
                    "rating": 4.3,
                    "user_ratings_total": 14560,
                    "types": ["beach", "tourist_attraction"],
                    "location": {"lat": 15.5439, "lng": 73.7550}
                },
                {
                    "name": "Chapora Fort",
                    "address": "Chapora, North Goa, Goa",
                    "rating": 4.4,
                    "user_ratings_total": 7890,
                    "types": ["fort", "historical", "viewpoint"],
                    "location": {"lat": 15.6048, "lng": 73.7364}
                }
            ],
            "kerala": [
                {
                    "name": "Munnar Tea Gardens",
                    "address": "Munnar, Idukki District, Kerala",
                    "rating": 4.7,
                    "user_ratings_total": 18920,
                    "types": ["nature", "tea_plantation", "tourist_attraction"],
                    "location": {"lat": 10.0889, "lng": 77.0595}
                },
                {
                    "name": "Alleppey Backwaters",
                    "address": "Alappuzha, Kerala 688001",
                    "rating": 4.8,
                    "user_ratings_total": 21340,
                    "types": ["nature", "backwaters", "houseboat", "tourist_attraction"],
                    "location": {"lat": 9.4981, "lng": 76.3388}
                },
                {
                    "name": "Fort Kochi",
                    "address": "Fort Kochi, Kochi, Kerala 682001",
                    "rating": 4.5,
                    "user_ratings_total": 16780,
                    "types": ["historical", "heritage", "tourist_attraction"],
                    "location": {"lat": 9.9647, "lng": 76.2428}
                },
                {
                    "name": "Athirapally Waterfalls",
                    "address": "Athirappilly, Thrissur, Kerala",
                    "rating": 4.6,
                    "user_ratings_total": 14230,
                    "types": ["waterfall", "nature", "tourist_attraction"],
                    "location": {"lat": 10.2850, "lng": 76.5700}
                }
            ],
            "himachal pradesh": [
                {
                    "name": "Rohtang Pass",
                    "address": "Manali-Leh Highway, Himachal Pradesh",
                    "rating": 4.6,
                    "user_ratings_total": 12450,
                    "types": ["mountain_pass", "scenic", "adventure"],
                    "location": {"lat": 32.3726, "lng": 77.2490}
                },
                {
                    "name": "Mall Road Shimla",
                    "address": "The Mall, Shimla, Himachal Pradesh 171001",
                    "rating": 4.4,
                    "user_ratings_total": 18920,
                    "types": ["shopping", "tourist_attraction"],
                    "location": {"lat": 31.1033, "lng": 77.1722}
                }
            ]
        }
        
        destination_lower = destination.lower()
        for key in mock_places:
            if key in destination_lower or destination_lower in key:
                return mock_places[key]
        
        return mock_places["goa"]
    
    def _get_mock_restaurants(self, destination: str) -> List[Dict[str, Any]]:
        """Mock restaurants with Indian names"""
        return [
            {
                "name": "Sattvam - Pure Veg Restaurant",
                "address": f"Main Market, {destination}",
                "rating": 4.3,
                "user_ratings_total": 1250,
                "types": ["restaurant", "vegetarian", "north_indian"],
                "location": {"lat": 0, "lng": 0},
                "price_level": 2
            },
            {
                "name": "Coastal Kitchen",
                "address": f"Beach Road, {destination}",
                "rating": 4.5,
                "user_ratings_total": 2340,
                "types": ["restaurant", "seafood", "coastal"],
                "location": {"lat": 0, "lng": 0},
                "price_level": 2
            },
            {
                "name": "The Local Thali House",
                "address": f"City Center, {destination}",
                "rating": 4.4,
                "user_ratings_total": 1890,
                "types": ["restaurant", "thali", "indian"],
                "location": {"lat": 0, "lng": 0},
                "price_level": 1
            },
            {
                "name": "Green Leaf Cafe",
                "address": f"Market Square, {destination}",
                "rating": 4.2,
                "user_ratings_total": 980,
                "types": ["cafe", "vegetarian", "healthy"],
                "location": {"lat": 0, "lng": 0},
                "price_level": 2
            }
        ]


# Singleton instance
travel_api = TravelAPIService()
