import asyncio
import httpx
import json

async def test_backend_response():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:5001/api/plan/create",
            json={
                "query": "Plan a 1-day food tour in Indiranagar, Bangalore",
                "userId": "test-user"
            },
            timeout=30.0
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Response received")
            print(f"Destination: {data.get('destination')}")
            
            if 'itinerary' in data and len(data['itinerary']) > 0:
                day1 = data['itinerary'][0]
                print(f"\nDay 1 has {len(day1.get('activities', []))} activities:")
                
                for i, activity in enumerate(day1.get('activities', [])[:5], 1):
                    print(f"{i}. {activity.get('name')} - Type: {activity.get('type')}")
                
                # Save full response to file for inspection
                with open('api_response.json', 'w') as f:
                    json.dump(data, f, indent=2)
                print("\n✅ Full response saved to api_response.json")
            else:
                print("❌ No itinerary in response")
        else:
            print(f"❌ Error: {response.status_code}")

if __name__ == "__main__":
    asyncio.run(test_backend_response())
