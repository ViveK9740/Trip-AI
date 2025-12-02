import asyncio
from agents.nlp_agent import nlp_agent

async def test_nlp_parsing():
    print("🧪 Testing NLP Agent with Structured Preferences...")
    
    # Test Case 1: Full structured preferences
    preferences = {
        "destination": "Manali",
        "duration": 5,
        "budget": 25000,
        "adults": 2,
        "children": 1,
        "foodPreference": "vegetarian",
        "transportMode": "own_vehicle",
        "nightTravel": "no",
        "accommodationType": "luxury",
        "travelStyle": "adventure"
    }
    
    query = "Plan a trip to Manali"
    
    print(f"\n📝 Query: '{query}'")
    print(f"📋 Preferences: {preferences}")
    
    result = await nlp_agent.process(query, preferences)
    
    print("\n🔍 Result:")
    print(f"Destination: {result['destination']}")
    print(f"Duration: {result['duration']['days']} days")
    print(f"Budget: ₹{result['budget']}")
    print(f"Travelers: {result['travelers']}")
    print(f"Preferences: {result['preferences']}")
    
    # Verification
    assert result['destination'] == "Manali"
    assert result['duration']['days'] == 5
    assert result['budget'] == 25000
    assert result['travelers']['adults'] == 2
    assert result['preferences']['transport_mode'] == "own_vehicle"
    assert result['preferences']['accommodation_type'] == "luxury"
    
    print("\n✅ Test Passed!")

if __name__ == "__main__":
    asyncio.run(test_nlp_parsing())
