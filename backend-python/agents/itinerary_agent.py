from typing import Dict, Any, List
from datetime import datetime, timedelta
from services.llm_service import llm_service
from services.travel_api import travel_api
from services.booking_service import booking_service
from utils.logger import log_data


class ItineraryAgent:
    """
    Itinerary Agent
    Creates detailed day-wise travel itineraries
    """
    
    async def process(self, trip_details: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process trip details and create itinerary"""
        print("📅 Itinerary Agent: Creating itinerary...")
        
        try:
            # Get travel style preference
            travel_style = trip_details.get("preferences", {}).get("travel_style", "balanced")
            print(f"🎨 Travel Style Detected: {travel_style}")
            
            # Fetch places data from travel API - ADJUST CATEGORIES BASED ON TRAVEL STYLE
            place_categories = self._get_categories_for_style(travel_style)
            
            places = []
            for category, limit in place_categories.items():
                category_places = await travel_api.search_places(trip_details["destination"], category)
                # Take limited results per category based on priority
                places.extend(category_places[:limit])
            
            # Remove duplicates based on name
            unique_places = {p["name"]: p for p in places}.values()
            places = list(unique_places)[:30]  # Increased to 30 for more variety
            
            print(f"📍 Diverse Attractions fetched: {len(places)} items (from {len(place_categories)} categories)")
            
            # Fetch fewer restaurants (only for meal planning)
            restaurants = await travel_api.search_restaurants(
                trip_details["destination"],
                trip_details["preferences"].get("dietary", [])[0] if trip_details["preferences"].get("dietary") else "any"
            )
            restaurants = restaurants[:5]  # Limit to 5 restaurants only
            print(f"🍽️ Restaurants fetched: {len(restaurants)} items (limited for meals)")
            
            # Fetch fewer hotels (only for accommodation reference)
            hotels = await travel_api.search_hotels(
                trip_details["destination"],
                trip_details["preferences"].get("accommodation_type", "mid_range")
            )
            hotels = hotels[:3]  # Limit to 3 hotels only
            print(f"🏨 Hotels fetched: {len(hotels)} items (limited for accommodation)")
            
            # Organize places by geographic clusters for route optimization
            clustered_places = self._cluster_places_by_location(places)
            print(f"🗺️  Organized {len(places)} attractions into geographic clusters")
            
            # Combine data for LLM with clustering info
            places_data = [
                {**p, "category": "attraction", "cluster": self._get_place_cluster(p, clustered_places)} 
                for p in places
            ] + [
                {**r, "category": "restaurant"} for r in restaurants
            ] + [
                {**h, "category": "hotel"} for h in hotels
            ]
            print(f"📦 Total places for Gemini: {len(places_data)} items")
            log_data("PLACES DATA SENT TO GEMINI", places_data)
            if places_data:
                print(f"🔍 Sample place: {places_data[0].get('name')}")
            
            # Generate route-optimized itinerary using LLM
            itinerary_data = await llm_service.generate_itinerary(
                trip_details, 
                places_data,
                clustered_places  # Pass clustering info for route optimization
            )
            log_data("GEMINI ITINERARY RESPONSE", itinerary_data)
            
            # Structure and enrich the itinerary
            itinerary = self._structure_itinerary(itinerary_data, trip_details)
            
            print(f"✅ Itinerary Agent: Created {len(itinerary)}-day itinerary")
            return itinerary
            
        except Exception as e:
            import traceback
            error_msg = f"❌ ITINERARY AGENT CRASHED: {str(e)}"
            print("\n" + "="*50)
            print(error_msg)
            print("="*50)
            print(f"Full traceback:")
            traceback.print_exc()
            print("="*50 + "\n")
            
            log_data("ITINERARY AGENT EXCEPTION", {"error": str(e), "traceback": traceback.format_exc()})
            
            # Fallback to template-based itinerary
            print("⚠️ FALLING BACK TO TEMPLATE DATA DUE TO ERROR")
            return self._create_template_itinerary(trip_details)
    
    def _structure_itinerary(
        self, 
        itinerary_data: Dict[str, Any], 
        trip_details: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Structure itinerary data with proper formatting"""
        # Handle both list format (from Gemini) and dict format
        if isinstance(itinerary_data, list):
            days = itinerary_data
        else:
            days = itinerary_data.get("days", [])
        
        structured = []
        for index, day in enumerate(days):
            activities = day.get("activities", [])
            
            # Calculate estimated costs
            total_cost = sum(
                self._estimate_activity_cost(activity, trip_details["budget"])
                for activity in activities
            )
            
            structured.append({
                "day": index + 1,
                "date": self._calculate_date(trip_details["duration"].get("start_date"), index),
                "activities": [
                    {
                        "time": activity.get("time") or self._suggest_time(activity.get("type")),
                        "type": activity.get("type", "sightseeing"),
                        "name": activity.get("name"),
                        "description": activity.get("description", ""),
                        "location": activity.get("location", {"name": activity.get("name")}),
                        "estimatedCost": self._estimate_activity_cost(activity, trip_details["budget"]),
                        "duration": activity.get("duration", "2 hours"),
                        "tips": activity.get("tips", ""),
                        "booking": booking_service.generate_booking_for_activity(
                            activity, 
                            trip_details["destination"]
                        )
                    }
                    for activity in activities
                ],
                "totalCost": round(total_cost),
                "summary": day.get("summary", f"Day {index + 1} exploring {trip_details['destination']}")
            })
        
        return structured
    
    def _estimate_activity_cost(self, activity: Dict, total_budget: float) -> float:
        """Estimate cost for an activity with realistic percentages"""
        # More realistic cost allocation
        cost_map = {
            "sightseeing": total_budget * 0.08,  # 8% per attraction
            "food": total_budget * 0.15,  # 15% per meal (realistic for food tours)
            "Restaurant": total_budget * 0.15,  # Handle capitalized type from Gemini
            "activity": total_budget * 0.12,  # 12% for activities
            "travel": total_budget * 0.05,  # 5% for transport
            "rest": 0
        }
        activity_type = activity.get("type", "sightseeing")
        base_cost = cost_map.get(activity_type, total_budget * 0.08)
        
        # Ensure minimum reasonable cost
        if activity_type in ["food", "Restaurant"] and base_cost < 300:
            base_cost = 300  # Minimum ₹300 for a meal
        
        return round(base_cost)
    
    def _suggest_time(self, activity_type: str) -> str:
        """Suggest time based on activity type"""
        time_map = {
            "sightseeing": "10:00 AM",
            "food": "01:00 PM",
            "Restaurant": "01:00 PM",  # Handle capitalized type
            "activity": "03:00 PM",
            "travel": "09:00 AM",
            "rest": "07:00 PM"
        }
        return time_map.get(activity_type, "10:00 AM")
    
    def _calculate_date(self, start_date: str, day_index: int):
        """Calculate date for each day"""
        if not start_date:
            return None
        
        try:
            date = datetime.fromisoformat(start_date) if isinstance(start_date, str) else start_date
            date = date + timedelta(days=day_index)
            return date.isoformat()
        except:
            return None
    
    def _cluster_places_by_location(self, places: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Cluster places into geographic zones based on coordinates.
        Uses simple lat/lng grouping for route optimization.
        """
        if not places:
            return {}
        
        # Simple clustering: group by rounded lat/lng (approximate zones)
        clusters = {}
        cluster_names = ["North", "South", "East", "West", "Central"]
        
        # Calculate center point
        valid_places = [p for p in places if p.get("location", {}).get("lat") and p.get("location", {}).get("lng")]
        if not valid_places:
            return {"Central": places}
        
        avg_lat = sum(p["location"]["lat"] for p in valid_places) / len(valid_places)
        avg_lng = sum(p["location"]["lng"] for p in valid_places) / len(valid_places)
        
        # Cluster based on position relative to center
        for place in places:
            loc = place.get("location", {})
            lat, lng = loc.get("lat", avg_lat), loc.get("lng", avg_lng)
            
            if not lat or not lng:
                cluster_key = "Central"
            else:
                # Determine zone
                lat_diff = lat - avg_lat
                lng_diff = lng - avg_lng
                
                if abs(lat_diff) < 0.01 and abs(lng_diff) < 0.01:
                    cluster_key = "Central"
                elif abs(lat_diff) > abs(lng_diff):
                    cluster_key = "North" if lat_diff > 0 else "South"
                else:
                    cluster_key = "East" if lng_diff > 0 else "West"
            
            if cluster_key not in clusters:
                clusters[cluster_key] = []
            clusters[cluster_key].append(place)
        
        print(f"   🗺️  Geographic zones: {', '.join([f'{k}({len(v)})' for k, v in clusters.items()])}")
        return clusters
    
    def _get_place_cluster(self, place: Dict[str, Any], clusters: Dict[str, List[Dict[str, Any]]]) -> str:
        """Get the cluster name for a place"""
        for cluster_name, cluster_places in clusters.items():
            if any(p["name"] == place["name"] for p in cluster_places):
                return cluster_name
        return "Central"
    
    def _create_template_itinerary(self, trip_details: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create template-based itinerary as fallback"""
        destination = trip_details["destination"]
        days = trip_details["duration"]["days"]
        preferences = trip_details["preferences"]
        
        itinerary = []
        for i in range(days):
            itinerary.append({
                "day": i + 1,
                "date": self._calculate_date(trip_details["duration"].get("start_date"), i),
                "activities": [
                    {
                        "time": "09:00 AM",
                        "type": "travel",
                        "name": "Morning Travel",
                        "description": "Start the day with local transportation",
                        "estimatedCost": 200,
                        "duration": "1 hour"
                    },
                    {
                        "time": "10:30 AM",
                        "type": "sightseeing",
                        "name": f"Popular Attraction in {destination}",
                        "description": "Visit a famous tourist spot",
                        "estimatedCost": 500,
                        "duration": "2 hours"
                    },
                    {
                        "time": "01:00 PM",
                        "type": "food",
                        "name": "Vegetarian Restaurant" if "veg" in preferences.get("dietary", []) 
                               else "Local Restaurant",
                        "description": "Enjoy local cuisine",
                        "estimatedCost": 400,
                        "duration": "1 hour"
                    },
                    {
                        "time": "03:00 PM",
                        "type": "activity" if "beaches" in preferences.get("activities", []) 
                               else "sightseeing",
                        "name": "Beach Activities" if "beaches" in preferences.get("activities", [])
                               else "Cultural Tour",
                        "description": "Afternoon exploration",
                        "estimatedCost": 600,
                        "duration": "3 hours"
                    },
                    {
                        "time": "07:00 PM",
                        "type": "food",
                        "name": "Dinner",
                        "description": "Evening meal at a nice restaurant",
                        "estimatedCost": 500,
                        "duration": "1 hour"
                    }
                ],
                "totalCost": 2200,
                "summary": f"Day {i + 1}: Exploring {destination}"
            })
        
        return itinerary
    
    def _get_categories_for_style(self, travel_style: str) -> Dict[str, int]:
        """Return place categories optimized for specific travel style"""
        
        if travel_style == "cultural":
            # CULTURAL STYLE: Focus on heritage, temples, museums, monuments
            return {
                # Historical & Cultural (HIGHEST PRIORITY)
                "temple": 10, "fort": 10, "palace": 10, "monument": 10, 
                "heritage site": 10, "museum": 8, "historical site": 8,
                "ancient temple": 8, "archaeological site": 8,
                # Some natural with cultural significance
                "sacred lake": 5, "holy river": 5,
                # Local cultural experiences
                "art gallery": 6, "cultural center": 6, "traditional market": 5,
                # Minimal modern attractions
                "viewpoint": 2, "park": 2
            }
        
        elif travel_style == "adventure":
            # ADVENTURE STYLE: Focus on thrilling activities, nature, sports
            return {
                # Adventure & Activities (HIGHEST PRIORITY)
                "adventure activity": 10, "water sports": 10, "trekking": 10,
                "wildlife sanctuary": 10, "national park": 10,
                # Natural attractions good for adventure
                "waterfall": 8, "hill station": 8, "viewpoint": 8, 
                "mountain": 8, "river": 8, "lake": 6,
                # Modern activities
                "amusement park": 7, "zoo": 6, "aquarium": 6,
                "cruise": 6, "paragliding": 8, "rafting": 8,
                # Minimal cultural/religious
                "fort": 3, "temple": 2
            }
        
        elif travel_style == "relaxed":
            # RELAXED STYLE: Focus on beaches, spas, peaceful spots, cafes
            return {
                # Peaceful & Relaxing (HIGHEST PRIORITY)
                "beach": 10, "lake": 10, "spa": 10, "resort": 8,
                "sunset point": 10, "garden": 8, "park": 8,
                "botanical garden": 8, "peaceful temple": 6,
                # Leisure activities
                "cafe": 8, "restaurant": 6, "viewpoint": 8,
                "shopping": 5, "market": 4,
                # Some light activities
                "boat ride": 7, "cruise": 7,
                # Minimal strenuous activities
                "monument": 3, "museum": 3, "fort": 2
            }
        
        else:  # balanced (default)
            # BALANCED STYLE: Good mix of everything
            return {
                # Natural attractions (HIGH PRIORITY)
                "beach": 8, "waterfall": 8, "lake": 6, "viewpoint": 8, "hill station": 6,
                # Historical & Cultural (MEDIUM PRIORITY)
                "fort": 5, "palace": 5, "monument": 4, "heritage site": 5, "museum": 4,
                # Religious (LOW PRIORITY)
                "temple": 3, "church": 2,
                # Entertainment & Activities (HIGH PRIORITY)
                "adventure activity": 7, "amusement park": 6, "zoo": 5, "aquarium": 5,
                "botanical garden": 5, "wildlife sanctuary": 6, "national park": 6,
                # Local experiences (MEDIUM PRIORITY)
                "market": 4, "shopping": 4, "cafe": 3, "local attraction": 6,
                # Modern attractions
                "casino": 4, "cruise": 5, "water sports": 6, "night club": 3
            }


# Singleton instance
itinerary_agent = ItineraryAgent()
