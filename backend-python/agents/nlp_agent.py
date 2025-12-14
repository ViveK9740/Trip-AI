import os
import re
from typing import Dict, Any, List, Optional
from services.llm_service import llm_service


class NLPAgent:
    """
    NLP Agent - Natural Language Processing
    Parses user queries to extract structured travel information
    """
    
    async def process(
        self, 
        user_query: str, 
        user_preferences: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Process user query and extract trip details"""
        print("🧠 NLP Agent: Parsing user query...")
        
        try:
            # Use LLM to parse the query
            parsed = await llm_service.parse_user_query(user_query, user_preferences or {})
            
            # Debug: Log what was parsed
            print(f"🔍 LLM Parsed Data:")
            print(f"   📍 Parsed Destination: {parsed.get('destination')}")
            print(f"   📝 Form Destination: {user_preferences.get('destination') if user_preferences else 'None'}")
            
            # Validate and enrich the parsed data
            # IMPORTANT: Use parsed destination from query if form destination is not explicitly provided
            # This allows query to override empty/missing form fields
            enriched = {
                "destination": parsed.get("destination") or user_preferences.get("destination"),
                "origin": user_preferences.get("origin"),
                "is_round_trip": user_preferences.get("isRoundTrip", False),  # Match frontend field name
                "duration": {
                    "days": int(user_preferences.get("duration") or parsed.get("duration", {}).get("days") or self._extract_days(user_query)),
                    "start_date": parsed.get("duration", {}).get("startDate"),
                    "end_date": parsed.get("duration", {}).get("endDate")
                },
                "budget": float(user_preferences.get("budget") or parsed.get("budget") or self._extract_budget(user_query)),
                "travelers": user_preferences.get("travelers") or {
                    "adults": int(parsed.get("travelers", {}).get("adults", 2)),
                    "children": int(parsed.get("travelers", {}).get("children", 0))
                },
                "preferences": {
                    # Merge form preferences with parsed ones, form takes priority
                    "dietary": user_preferences.get("preferences", {}).get("dietary") or parsed.get("preferences", {}).get("dietary") or [],
                    "activities": parsed.get("preferences", {}).get("activities") or self._extract_activities(user_query),
                    "transport_mode": user_preferences.get("preferences", {}).get("transport_mode", "flexible"),
                    "night_travel": user_preferences.get("preferences", {}).get("night_travel", False),
                    "accommodation_type": user_preferences.get("preferences", {}).get("accommodation_type", "mid_range"),
                    "travel_style": user_preferences.get("preferences", {}).get("travel_style", "balanced")
                },
                "event_details": parsed.get("event_details", {
                    "has_event": False
                })
            }
            
            # Log the preferences being used
            print(f"👤 User Preferences Applied:")
            print(f"   🏠 Origin: {enriched['origin']}")
            print(f"   🎯 Destination: {enriched['destination']}")
            print(f"   🔄 Round Trip: {enriched['is_round_trip']}")
            if enriched.get("event_details", {}).get("has_event"):
                print(f"   🎪 EVENT DETECTED: {enriched['event_details'].get('event_type', 'Unknown')} - {enriched['event_details'].get('event_name', 'N/A')}")
                print(f"   📍 Event Location: {enriched['event_details'].get('event_location', 'N/A')}")
                print(f"   📅 Event Schedule: {enriched['event_details'].get('event_schedule', 'N/A')}")
            print(f"   ⏱️  Duration: {enriched['duration']['days']} days")
            print(f"   💰 Budget: ₹{enriched['budget']}")
            print(f"   👥 Travelers: {enriched['travelers']['adults']} adults, {enriched['travelers']['children']} children")
            print(f"   ✨ Style: {enriched['preferences']['travel_style']}")
            print(f"   🏨 Accommodation: {enriched['preferences']['accommodation_type']}")
            print(f"   🚌 Transport: {enriched['preferences']['transport_mode']}")
            
            print(f"✅ NLP Agent: Parsed successfully - {enriched}")
            return enriched
            
        except Exception as e:
            print(f"❌ NLP Agent Error: {str(e)}")
            # Fallback to basic regex parsing
            return self._fallback_parsing(user_query, user_preferences or {})
    
    def _extract_days(self, query: str) -> int:
        """Extract number of days using regex as fallback"""
        day_match = re.search(r'(\d+)\s*[-]?\s*day', query, re.IGNORECASE)
        if day_match:
            return int(day_match.group(1))
        
        # Check for weekend (default 3 days)
        if re.search(r'weekend', query, re.IGNORECASE):
            return 3
        
        # Check for week
        if re.search(r'week', query, re.IGNORECASE):
            return 7
        
        return 3  # Default
    
    def _extract_budget(self, query: str) -> float:
        """Extract budget using regex as fallback"""
        # Try ₹ symbol or rs. or inr
        budget_match = re.search(r'(?:₹|rs\.?|inr)\s*(\d+(?:,\d+)*)', query, re.IGNORECASE)
        if budget_match:
            return float(budget_match.group(1).replace(',', ''))
        
        # Try "under X"
        under_match = re.search(r'under\s+(\d+(?:,\d+)*)', query, re.IGNORECASE)
        if under_match:
            return float(under_match.group(1).replace(',', ''))
        
        return 15000.0  # Default budget
    
    def _extract_dietary(self, query: str) -> List[str]:
        """Extract dietary preferences"""
        dietary = []
        query_lower = query.lower()
        
        if 'veg' in query_lower and 'non-veg' not in query_lower:
            dietary.append('veg')
        if 'vegan' in query_lower:
            dietary.append('vegan')
        if 'non-veg' in query_lower:
            dietary.append('non-veg')
        if 'jain' in query_lower:
            dietary.append('jain')
        
        return dietary
    
    def _extract_activities(self, query: str) -> List[str]:
        """Extract activity preferences"""
        activities = []
        query_lower = query.lower()
        
        if 'beach' in query_lower:
            activities.append('beaches')
        if 'trek' in query_lower:
            activities.append('trekking')
        if 'adventure' in query_lower:
            activities.append('adventure')
        if any(word in query_lower for word in ['cultural', 'heritage', 'temple']):
            activities.append('cultural')
        if any(word in query_lower for word in ['nightlife', 'party', 'club']):
            activities.append('nightlife')
        if any(word in query_lower for word in ['nature', 'wildlife']):
            activities.append('nature')
        
        return activities
    
    def _fallback_parsing(
        self, 
        query: str, 
        user_preferences: Dict
    ) -> Dict[str, Any]:
        """Fallback parsing without LLM"""
        # Extract destination (basic - first capitalized word sequence after "to")
        dest_match = re.search(r'to\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', query)
        destination = dest_match.group(1) if dest_match else 'Goa'
        
        return {
            "destination": destination,
            "duration": {
                "days": self._extract_days(query),
                "start_date": None,
                "end_date": None
            },
            "budget": self._extract_budget(query),
            "preferences": {
                "dietary": self._extract_dietary(query) or user_preferences.get("dietary", []),
                "activities": self._extract_activities(query) or user_preferences.get("activities", [])
            }
        }


# Singleton instance
nlp_agent = NLPAgent()
