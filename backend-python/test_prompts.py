import asyncio
import httpx
import json

async def test_different_prompts():
    test_queries = [
        "Plan a 3-day adventure trip to Manali with trekking and camping",
        "I want a romantic 2-day getaway in Udaipur under 20000 rupees",
        "Weekend trip to Goa for a family of 4, budget friendly"
    ]
    
    async with httpx.AsyncClient() as client:
        for i, query in enumerate(test_queries, 1):
            print(f"\n{'='*60}")
            print(f"TEST {i}: {query}")
            print('='*60)
            
            try:
                response = await client.post(
                    "http://localhost:5001/api/plan/create",
                    json={"query": query, "userId": "test-user"},
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Success!")
                    print(f"Destination: {data.get('destination')}")
                    print(f"Duration: {data.get('duration', {}).get('days')} days")
                    print(f"Budget: ₹{data.get('budget')}")
                    
                    if 'itinerary' in data:
                        print(f"\nItinerary Preview:")
                        for day in data['itinerary'][:1]:  # Show first day
                            print(f"  Day {day['day']}: {len(day.get('activities', []))} activities")
                            for act in day.get('activities', [])[:3]:
                                print(f"    - {act.get('name')}")
                else:
                    print(f"❌ Error: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Exception: {str(e)}")
            
            await asyncio.sleep(2)  # Wait between requests

if __name__ == "__main__":
    asyncio.run(test_different_prompts())
