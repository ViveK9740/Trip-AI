import google.generativeai as genai
import os
import json
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class LLMService:
    """
    LLM Service for AI agent operations
    Centralized service for all Gemini API calls
    """
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("⚠️ GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        # Use gemini-2.5-flash (confirmed available model)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    async def generate_completion(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Generate completion from Gemini"""
        try:
            # Convert OpenAI-style messages to Gemini history
            prompt = self._convert_messages_to_prompt(messages)
            
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens
                )
            )
            return response.text
        except Exception as e:
            print(f"Gemini API Error: {str(e)}")
            raise Exception(f"LLM Service Error: {str(e)}")
    
    async def generate_json(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Generate structured JSON response"""
        try:
            prompt = self._convert_messages_to_prompt(messages)
            
            # Use JSON mode for Gemini
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    response_mime_type="application/json"
                )
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"Gemini JSON Error: {str(e)}")
            # Fallback: try to extract JSON from text if strict JSON mode fails
            try:
                text = response.text
                start = text.find('{')
                end = text.rfind('}') + 1
                if start != -1 and end != -1:
                    return json.loads(text[start:end])
            except:
                pass
            raise Exception(f"LLM JSON Error: {str(e)}")

    def _convert_messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert OpenAI messages format to a single prompt string for Gemini"""
        # Gemini 1.5 Flash handles system instructions well, but for simplicity
        # we'll combine them into a structured prompt
        prompt_parts = []
        
        for msg in messages:
            role = msg["role"].upper()
            content = msg["content"]
            prompt_parts.append(f"[{role}]: {content}")
            
        return "\n\n".join(prompt_parts)
    
    async def parse_user_query(
        self, 
        query: str, 
        user_preferences: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Parse user query to extract travel details"""
        messages = [
            {
                "role": "system",
                "content": """You are a travel query parser. Extract structured information from user's travel request.

CRITICAL: Identify the PRIMARY DESTINATION carefully:
- If query mentions "from X to Y", the destination is Y (where user is GOING)
- If query mentions event/purpose at a location, that location is the destination
- Don't confuse origin (starting point) with destination (where they're going)

Return JSON with: 
- destination (string: MAIN place they want to visit/reach)
- origin (string: where they are starting from, if mentioned)
- duration (object with days, startDate, endDate)
- budget (number)
- travelers (object with adults, children)
- event_details (object: if this is for a specific event like hackathon, conference, wedding, etc.)
  * has_event (boolean: true if trip is for a specific event)
  * event_type (string: hackathon, conference, wedding, meeting, etc.)
  * event_name (string: name of the event)
  * event_location (string: specific venue/address of the event)
  * event_schedule (object with startDateTime, endDateTime in ISO format)
  * return_constraints (string: any time constraints for return journey)
- preferences (object with:
    - dietary (array: veg, non-veg, vegan)
    - transport_mode (public_transport, own_vehicle, rental, flexible)
    - accommodation_type (budget, mid_range, luxury)
    - travel_style (relaxed, balanced, adventure)
    - activities (array of interests)
    - night_travel (boolean)
)

EXAMPLES:
Query: "Trip from Mumbai to Goa" → destination: "Goa", origin: "Mumbai", event_details: {has_event: false}
Query: "Visiting Jaipur for 3 days" → destination: "Jaipur", event_details: {has_event: false}
Query: "Hackathon in Hyderabad, starting from Bangalore" → destination: "Hyderabad", origin: "Bangalore", event_details: {has_event: true, event_type: "hackathon", event_location: "Hyderabad"}
Query: "Conference at IIT Delhi from Dec 20-22, need to be back by 23rd morning" → destination: "Delhi", event_details: {has_event: true, event_type: "conference", event_name: "IIT Delhi conference", event_schedule: {startDateTime: "2025-12-20T09:00:00", endDateTime: "2025-12-22T17:00:00"}, return_constraints: "must be back by Dec 23rd morning"}

If information is missing, use null. For dates, use ISO format YYYY-MM-DD."""
            },
            {
                "role": "user",
                "content": f"""User query: "{query}"

User's stored preferences: {json.dumps(user_preferences or {})}

IMPORTANT: 
1. Identify the DESTINATION (where they want to GO/VISIT)
2. Identify the ORIGIN (where they are starting FROM) if mentioned
3. Extract specific dates if mentioned
4. Calculate duration based on dates or explicit mentions

Extract all travel details as JSON."""
            }
        ]
        
        return await self.generate_json(messages)
    
    async def generate_itinerary(
        self, 
        trip_details: Dict[str, Any], 
        places_data: List[Dict],
        clusters: Dict[str, List[Dict]] = None
    ) -> Dict[str, Any]:
        """Generate route-optimized itinerary suggestions"""
        messages = [
            {
                "role": "system",
                "content": f"""You are an expert travel planner. Create a detailed day-wise itinerary.
Return JSON with array of days, each containing: 
- day (number)
- summary (brief description of the day)
- activities (array with time, type, name, description, duration, tips, location object).

🎯 TRIP TYPE DETECTION:
{"EVENT-FOCUSED TRIP" if trip_details.get('event_details', {}).get('has_event', False) else "LEISURE/TOURISM TRIP"}

{"⚠️ CRITICAL - EVENT-FOCUSED TRIP MODE:" if trip_details.get('event_details', {}).get('has_event', False) else ""}
{"This is NOT a tourism trip! User is attending a specific event." if trip_details.get('event_details', {}).get('has_event', False) else ""}
{"Event Details:" if trip_details.get('event_details', {}).get('has_event', False) else ""}
{f"- Event Type: {trip_details.get('event_details', {}).get('event_type', 'N/A')}" if trip_details.get('event_details', {}).get('has_event', False) else ""}
{f"- Event Location: {trip_details.get('event_details', {}).get('event_location', 'N/A')}" if trip_details.get('event_details', {}).get('has_event', False) else ""}
{f"- Event Schedule: {trip_details.get('event_details', {}).get('event_schedule', 'N/A')}" if trip_details.get('event_details', {}).get('has_event', False) else ""}
{f"- Return Constraints: {trip_details.get('event_details', {}).get('return_constraints', 'N/A')}" if trip_details.get('event_details', {}).get('has_event', False) else ""}

{"EVENT TRIP ITINERARY RULES:" if trip_details.get('event_details', {}).get('has_event', False) else ""}
{"1. FOCUS ON THE EVENT - Block out exact event hours (make event the PRIMARY activity)" if trip_details.get('event_details', {}).get('has_event', False) else ""}
{"2. Plan travel to reach event venue BEFORE event start time with buffer" if trip_details.get('event_details', {}).get('has_event', False) else ""}
{"3. Only add minimal sightseeing if there's genuinely free time (early mornings/late evenings)" if trip_details.get('event_details', {}).get('has_event', False) else ""}
{"4. Respect return constraints - plan departure to meet return deadline" if trip_details.get('event_details', {}).get('has_event', False) else ""}
{"5. Keep accommodations close to event venue for convenience" if trip_details.get('event_details', {}).get('has_event', False) else ""}
{"6. During event hours: Schedule meals near event venue, no sightseeing" if trip_details.get('event_details', {}).get('has_event', False) else ""}

CRITICAL INSTRUCTIONS:
1. Include Hotel Check-in on Day 1 and Check-out on last day.
2. If Origin is provided, plan travel from Origin to Destination on Day 1 (Activity Type: 'travel').
3. If Round Trip is true, plan return travel from Destination to Origin on the last day (Activity Type: 'travel').
4. Plan Breakfast, Lunch, and Dinner for every day.

EXTREMELY IMPORTANT - RESTAURANT RULES:
5. For ALL food activities, you MUST use ONLY restaurants from the "Available Places" list below where category='restaurant'.
6. FORBIDDEN: You are ABSOLUTELY PROHIBITED from creating ANY restaurant names. 
7. FORBIDDEN EXAMPLES (DO NOT USE THESE OR SIMILAR):
   - "The Local Thali House"
   - "Street Food Stall"
   - "Local Market Restaurant"
   - "Traditional Eatery"
   - "Roadside Dhaba"
   - Any name with "Local", "Traditional", "Street", or generic descriptors
8. If a restaurant name is not in the provided "Available Places" list, DO NOT USE IT.
9. If you cannot find enough restaurants in the list, repeat existing restaurants rather than inventing names.
10. Every restaurant name MUST have a matching entry in the "Available Places" JSON with category='restaurant'.

HOTEL RULES:
11. For hotels, use ONLY hotels from "Available Places" where category='hotel'. DO NOT invent hotel names.

ATTRACTIONS RULES:
12. For sights eeing, use ONLY specific places from "Available Places" with actual names and addresses.
13. DO NOT use generic descriptions like "Visit a Local Temple" or "Explore Local Market". Use specific place names from the data.

OTHER RULES:
14. DO NOT repeat the same restaurant for consecutive meals unless absolutely no other option exists.
15. Ensure logical flow: breakfast -> morning activity -> lunch -> afternoon activity -> dinner.
16. Include travel time between locations.
17. Respect user's travel style.
18. For "Relax" activities, be specific (e.g., "Relax at hotel pool", "Sunset walk").

Activity Types: 'hotel', 'food', 'sightseeing', 'travel', 'rest'.

VALIDATION: Before returning your response, verify that EVERY restaurant name appears in the Available Places list. If it doesn't, you have made an error and must fix it."""
            },
            {
                "role": "user",
                "content": f"""Create {trip_details['duration']['days']}-day {'EVENT-FOCUSED' if trip_details.get('event_details', {}).get('has_event', False) else 'DIVERSE & OPTIMIZED'} itinerary for {trip_details['destination']}.

🎯 GOAL: {'Focus on event attendance with practical logistics! This is NOT a sightseeing trip.' if trip_details.get('event_details', {}).get('has_event', False) else 'Create a realistic, well-rounded itinerary with diverse experiences and optimized routes!'}

📋 TRIP DETAILS:
- Origin: {trip_details.get('origin', 'Not specified')}
- Destination: {trip_details['destination']}
- Round Trip: {trip_details.get('is_round_trip', False)}
- Duration: {trip_details['duration']['days']} days
- Budget: ₹{trip_details['budget']}
- Travelers: {trip_details.get('travelers', {}).get('adults', 2)} adults, {trip_details.get('travelers', {}).get('children', 0)} children

👤 USER PREFERENCES (MUST RESPECT):
- Travel Style: {trip_details.get('preferences', {}).get('travel_style', 'balanced')}
  * relaxed = More breaks, leisurely pace, fewer attractions per day (3-4)
  * balanced = Good mix, moderate pace, standard attractions (4-5)
  * adventure = Packed schedule, fast pace, maximum attractions (5-6)
  * cultural = Focus on historical/religious sites, museums, heritage
  
- Accommodation: {trip_details.get('preferences', {}).get('accommodation_type', 'mid_range')}
  * budget = Hostels, budget hotels (allocate less budget for stay)
  * mid_range = 3-4 star hotels (balanced budget)
  * luxury = 5-star hotels/resorts (allocate more budget for stay)
  
- Transport Mode: {trip_details.get('preferences', {}).get('transport_mode', 'flexible')}
  * public = Use buses, trains (mention in tips)
  * own_vehicle = Driving own car (mention parking)
  * rental = Rented car/bike (mention pickup points)
  * flight = Flights for long distance
  
- Night Travel: {trip_details.get('preferences', {}).get('night_travel', False)}
  * If True: Can plan overnight journeys to save time
  * If False: All travel during daytime only
  
- Dietary: {trip_details.get('preferences', {}).get('dietary', [])}
  * Use this to select restaurants (veg/non-veg/vegan)

🎨 CUSTOMIZE BASED ON PREFERENCES:
1. Match travel_style pace (relaxed/balanced/adventure/cultural)
2. Adjust number of attractions per day accordingly
3. If cultural style → prioritize temples, monuments, museums, heritage sites
4. If adventure style → include adventure activities, viewpoints, trekking
5. If relaxed style → add spa, beach relaxation, sunset viewing spots
6. Select restaurants matching dietary preferences
7. Mention transport tips based on transport_mode

Available Places (PRIORITIZE category='attraction'):
{json.dumps(places_data[:100])}

📊 GEOGRAPHIC CLUSTERS AVAILABLE:
{json.dumps({k: [p["name"] for p in v] for k, v in (clusters or {}).items()}, indent=2) if clusters else "No clustering data"}

⚠️ CRITICAL REQUIREMENTS:
1. **DIVERSE EXPERIENCES**: Mix different types of places
   - Natural attractions: Beaches, waterfalls, viewpoints, lakes (40%)
   - Cultural/Historical: Forts, monuments, museums, heritage sites (25%)
   - Activities: Adventure, water sports, markets, shopping (20%)
   - Religious sites: Only 2-3 temples max per trip (15%)

2. **RESPECT USER PREFERENCES**: Adjust attractions count based on travel_style
   - Relaxed: 3-4 places/day, more breaks, beach time, cafes
   - Balanced: 4-5 places/day, moderate pace, good mix
   - Adventure: 5-6 places/day, packed schedule, adventure activities
   - Cultural: Focus quality historical sites, museums, fewer places

3. **ROUTE OPTIMIZATION IS MANDATORY**:
   - Group places by cluster/geographic zone
   - Visit nearby places together on same day
   - Minimize backtracking and zigzag travel
   - Logical north→south or east→west progression

4. **REALISTIC TIMING**:
   - Account for travel time between places (15-45 min)
   - Give 1-2 hours per major attraction
   - Include breaks for meals (60-90 min)
   - Allow buffer time for delays

5. **USE ONLY REAL DATA**:
   - Every place name must match Available Places JSON
   - NEVER invent fake places or attractions
   - Use exact names and addresses provided

6. **MEAL PLANNING**:
   - Match restaurants to dietary preferences
   - Place restaurants strategically on route
   - Don't backtrack just for food

7. **PRACTICAL TIPS**:
   - Mention best time to visit (avoid crowds)
   - Suggest transport options based on preference
   - Add local insights and warnings
   - Include sunset/sunrise viewpoints where relevant

🗺️ ROUTE OPTIMIZATION EXAMPLES:
❌ BAD: North Beach → South Temple → North Fort → South Waterfall (zigzag, wasted time)
✅ GOOD: North Beach → North Fort → North Viewpoint → Nearby Restaurant (efficient, logical)

❌ BAD: Baga Beach → Dudhsagar Waterfall → Calangute Beach (far apart)
✅ GOOD: Baga Beach → Calangute Beach → Anjuna Beach (close together)

📅 SAMPLE DAY STRUCTURES:

RELAXED STYLE:
Day 1: Morning beach (2 hrs) → Beachside cafe (1 hr) → Coastal fort (1.5 hrs) → Lunch (1.5 hrs) → Viewpoint sunset (1 hr) → Hotel

BALANCED STYLE:
Day 1: Beach (1.5 hrs) → Fort (1 hr) → Market (1 hr) → Lunch (1 hr) → Museum (1 hr) → Waterfall (1.5 hrs) → Dinner

ADVENTURE STYLE:
Day 1: Early beach (1 hr) → Water sports (2 hrs) → Quick breakfast (30 min) → Fort (1 hr) → Viewpoint (1 hr) → Adventure activity (2 hrs) → Late lunch (45 min) → Sunset spot (1 hr)

CULTURAL STYLE:
Day 1: Heritage temple (2 hrs) → Historical monument (2 hrs) → Traditional lunch (1.5 hrs) → Museum (2 hrs) → Ancient fort (1.5 hrs)

🎯 CREATE A DIVERSE, ROUTE-OPTIMIZED, REALISTIC ITINERARY NOW!
Focus on: Natural beauty > Activities > Culture > Limited religious sites"""
            }
        ]
        
        return await self.generate_json(messages)
    
    async def validate_budget(
        self, 
        itinerary: List[Dict], 
        budget: float
    ) -> Dict[str, Any]:
        """Validate and adjust budget"""
        messages = [
            {
                "role": "system",
                "content": """You are a budget advisor. Review the itinerary and check if it fits within budget.
Return JSON with: withinBudget (boolean), totalEstimated (number), breakdown (object), adjustments (array of suggestions if over budget)."""
            },
            {
                "role": "user",
                "content": f"""Budget: ₹{budget}
Itinerary: {json.dumps(itinerary)}

Validate and provide breakdown."""
            }
        ]
        
        return await self.generate_json(messages)


# Singleton instance
llm_service = LLMService()
