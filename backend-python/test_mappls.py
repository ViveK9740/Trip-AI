import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def test_mappls():
    api_key = os.getenv("MAPPLS_API_KEY")
    print(f"API Key found: {'Yes' if api_key else 'No'}")
    if api_key:
        print(f"API Key (first 5 chars): {api_key[:5]}...")
    else:
        print("❌ No MAPPLS_API_KEY found in .env")
        return

    base_url = "https://atlas.mappls.com/api/places"
    destination = "Indiranagar, Bangalore"
    
    print(f"\nTesting Geocoding for: {destination}")
    async with httpx.AsyncClient() as client:
        try:
            # Attempt 1: Bearer Token (Already failed, but keeping for reference)
            # Attempt 2: Query Parameter 'key'
            print("Attempting with 'key' query parameter...")
            response = await client.get(
                f"{base_url}/geocode",
                params={"address": destination, "key": api_key},
                timeout=10.0
            )
            print(f"Geocode Status (Query Param): {response.status_code}")
            
            if response.status_code != 200:
                 # Attempt 3: 'license_key' query parameter
                print("Attempting with 'license_key' query parameter...")
                response = await client.get(
                    f"{base_url}/geocode",
                    params={"address": destination, "license_key": api_key},
                    timeout=10.0
                )
                print(f"Geocode Status (License Key): {response.status_code}")

            if response.status_code == 200:
                print(f"Geocode Response: {response.json()}")
            else:
                print(f"Geocode Error: {response.text}")

            # 2. Test Place Search
            print(f"\nTesting Place Search for 'restaurant' near {destination}")
            response = await client.get(
                f"{base_url}/search/json",
                params={
                    "query": f"restaurant near {destination}",
                    "region": "IND"
                },
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=10.0
            )
            print(f"Search Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                results = data.get("suggestedLocations", []) or data.get("results", [])
                print(f"Found {len(results)} places")
                if results:
                    print(f"First place: {results[0].get('placeName')}")
            else:
                print(f"Search Error: {response.text}")

        except Exception as e:
            print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_mappls())
