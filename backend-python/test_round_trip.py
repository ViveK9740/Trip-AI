import asyncio
import json
import logging
from agents.orchestrator import orchestrator
# from utils.logger import setup_logger # Not needed as it auto-configures on import

async def test_round_trip():
    # setup_logger()
    
    # Simulate user request
    query = "Plan a trip to Mandya"
    user_id = "test-user-roundtrip"
    
    # Detailed preferences with Origin and Round Trip
    preferences = {
        "origin": "Bengaluru",
        "is_round_trip": True,
        "destination": "Mandya",
        "duration": 2,
        "budget": 10000,
        "travelers": {"adults": 2, "children": 0},
        "preferences": {
            "transport_mode": "own_vehicle",
            "travel_style": "relaxed"
        }
    }
    
    print(f"Testing Round Trip: {preferences['origin']} -> {preferences['destination']} -> {preferences['origin']}")
    
    try:
        result = await orchestrator.create_travel_plan(query, user_id, preferences)
        
        if result["success"]:
            print("\n✅ Plan Created Successfully!")
            print(json.dumps(result["itinerary"], indent=2))
            
            # Verify Origin and Return
            itinerary = result["itinerary"]
            day1 = itinerary[0]
            last_day = itinerary[-1]
            
            has_departure = any("Bengaluru" in act.get("description", "") or "Bengaluru" in act.get("name", "") for act in day1["activities"])
            has_return = any("Bengaluru" in act.get("description", "") or "Bengaluru" in act.get("name", "") for act in last_day["activities"])
            
            if has_departure:
                print("✅ Found departure from Bengaluru on Day 1")
            else:
                print("❌ Missing departure from Bengaluru on Day 1")
                
            if has_return:
                print("✅ Found return to Bengaluru on Last Day")
            else:
                print("❌ Missing return to Bengaluru on Last Day")
                
        else:
            print("❌ Plan Creation Failed")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_round_trip())
