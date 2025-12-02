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
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
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
Return JSON with: 
- destination
- duration (object with days, startDate, endDate)
- budget (number)
- travelers (object with adults, children)
- preferences (object with:
    - dietary (array: veg, non-veg, vegan)
    - transport_mode (public_transport, own_vehicle, rental, flexible)
    - accommodation_type (budget, mid_range, luxury)
    - travel_style (relaxed, balanced, adventure)
    - activities (array of interests)
    - night_travel (boolean)
)
If information is missing, use null. For dates, use ISO format."""
            },
            {
                "role": "user",
                "content": f"""User query: "{query}"

User's stored preferences: {json.dumps(user_preferences or {})}

Extract travel details."""
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
                "content": """You are an expert travel planner. Create a detailed day-wise itinerary.
Return JSON with array of days, each containing: 
- day (number)
- summary (brief description of the day)
- activities (array with time, type, name, description, duration, tips, location object).

CRITICAL INSTRUCTIONS:
1. Include Hotel Check-in on Day 1 and Check-out on last day.
2. If Origin is provided ({trip_details.get('origin')}), plan travel from Origin to Destination on Day 1 (Activity Type: 'travel').
3. If Round Trip is true ({trip_details.get('is_round_trip')}), plan return travel from Destination to Origin on the last day (Activity Type: 'travel').
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
                "content": f"""Create {trip_details['duration']['days']}-day ATTRACTION-RICH itinerary for {trip_details['destination']}.

🎯 GOAL: Create an itinerary that MAXIMIZES tourist attractions and sightseeing experiences!

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

⚠️ CRITICAL REMINDERS:
1. **RESPECT USER PREFERENCES**: Adjust attractions count based on travel_style
   - Relaxed: 3-4 attractions/day, more breaks
   - Balanced: 4-5 attractions/day, moderate pace
   - Adventure: 5-6 attractions/day, packed schedule
   - Cultural: Focus heritage sites regardless of count
2. Focus 70-80% of schedule on TOURIST ATTRACTIONS (category='attraction')
3. **OPTIMIZE ROUTE**: Group attractions by cluster field - visit same zone together
4. Use ONLY real place names from the Available Places list above
5. NEVER create fake names - everything must match the JSON data
6. Keep meals SHORT (30-60 min) to maximize attraction time
7. Select restaurants matching dietary preferences (veg/non-veg/vegan)
8. Add transport tips based on transport_mode preference
9. **ROUTE EFFICIENCY**: Minimize travel time by intelligent zone planning

ROUTE OPTIMIZATION EXAMPLE:
❌ BAD: North attraction → South attraction → North attraction (zigzag)
✅ GOOD: North attraction → North attraction → North attraction (efficient)

PREFERENCE-BASED CUSTOMIZATION EXAMPLES:
✅ Relaxed Style: Morning attraction → Coffee break → One more attraction → Long lunch → Afternoon attraction → Rest
✅ Adventure Style: Early start → 3 morning attractions → Quick lunch → 3 afternoon attractions → Sunset spot
✅ Cultural Style: Temple 1 → Historical monument → Museum → Heritage site (focus quality over quantity)

START CREATING THE ROUTE-OPTIMIZED, PREFERENCE-CUSTOMIZED ITINERARY NOW!"""
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
