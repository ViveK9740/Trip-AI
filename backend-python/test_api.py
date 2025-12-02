import asyncio
import httpx

async def test_backend():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:5001/api/plan/create",
            json={
                "query": "Plan a 1-day food tour in Indiranagar, Bangalore",
                "userId": "test-user"
            },
            timeout=30.0
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            print(f"Destination: {data.get('destination')}")
            if 'itinerary' in data:
                print(f"Itinerary days: {len(data['itinerary'])}")
        else:
            print(f"Error: {response.text}")

if __name__ == "__main__":
    asyncio.run(test_backend())
