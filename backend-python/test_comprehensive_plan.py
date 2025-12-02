import asyncio
import json
from agents.orchestrator import orchestrator

async def test_comprehensive_plan():
    print("🧪 Testing Comprehensive Trip Planning...")
    
    # Simulate request from frontend with detailed preferences
    preferences = {
        "destination": "Udaipur",
        "duration": 3,
        "budget": 40000,
        "adults": 2,
        "children": 0,
        "foodPreference": "vegetarian",
        "transportMode": "rental",
        "nightTravel": "no",
        "accommodationType": "luxury",
        "travelStyle": "relaxed"
    }
    
    query = "Plan a relaxed 3-day luxury trip to Udaipur for 2 adults"
    
    print(f"\n📝 Query: '{query}'")
    print(f"📋 Preferences: {json.dumps(preferences, indent=2)}")
    
    try:
        # Call orchestrator directly
        result = await orchestrator.create_travel_plan(query, "test-user", preferences)
        
        print("\n✅ Plan Created Successfully!")
        print(f"Destination: {result['destination']}")
        print(f"Duration: {result['duration']['days']} days")
        print(f"Budget: ₹{result['budget']}")
        
        print("\n📅 Itinerary Highlights:")
        for day in result['itinerary']:
            print(f"\nDay {day['day']}: {day.get('summary', '')}")
            for activity in day['activities']:
                print(f"  - [{activity['type'].upper()}] {activity['name']} ({activity.get('time', '')})")
                if activity.get('booking'):
                    print(f"    🔗 Booking: {activity['booking']['label']} via {activity['booking'].get('primary', 'link')}")
        
        # Verify critical elements
        activities = [a for day in result['itinerary'] for a in day['activities']]
        
        # Check for hotels
        hotels = [a for a in activities if a['type'] in ['hotel', 'accommodation']]
        print(f"\n🏨 Hotels found: {len(hotels)}")
        
        # Check for meals
        meals = [a for a in activities if a['type'] in ['food', 'restaurant']]
        print(f"🍽️ Meals found: {len(meals)}")
        
        if len(hotels) > 0 and len(meals) >= 3:
            print("\n✅ SUCCESS: Itinerary includes hotels and multiple meals!")
        else:
            print("\n⚠️ WARNING: Itinerary might be missing hotels or meals.")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_comprehensive_plan())
