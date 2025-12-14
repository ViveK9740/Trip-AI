import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def test_search():
    print("Testing Mappls Search API...")
    
    client_id = os.getenv("MAPPLS_CLIENT_ID")
    client_secret = os.getenv("MAPPLS_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("❌ Missing credentials")
        return

    # 1. Get Token
    token_url = "https://outpost.mappls.com/api/security/oauth/token"
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            token_url,
            data={"grant_type": "client_credentials", "client_id": client_id, "client_secret": client_secret},
            timeout=10.0
        )
        if resp.status_code != 200:
            print(f"❌ Token Failed: {resp.text}")
            return
        
        access_token = resp.json().get("access_token")
        print("✅ Token received")

        # 2. Search
        destination = "Goa"
        query = "beaches in Goa"
        print(f"Searching for: '{query}'")
        
        search_url = "https://atlas.mappls.com/api/places/search/json"
        
        # Try Method A: Query Param (as in code)
        print("\n--- Method A: access_token in params ---")
        try:
            search_resp = await client.get(
                search_url,
                params={
                    "query": query,
                    "region": "IND",
                    "access_token": access_token
                }
            )
            print(f"Status: {search_resp.status_code}")
            if search_resp.status_code == 200:
                data = search_resp.json()
                results = data.get("suggestedLocations", [])
                print(f"Raw Results Count: {len(results)}")
                if results:
                    print(f"First Result: {results[0]}")
                    
                    # Test Filtering Logic from travel_api.py
                    filtered_count = 0
                    for place in results:
                        address = place.get("placeAddress", "") or place.get("address", "")
                        name = place.get("placeName", "") or place.get("name", "")
                        
                        destination_match = (destination.lower() in address.lower() or 
                                           destination.lower() in name.lower() or
                                           destination.split()[0].lower() in address.lower())
                        
                        if destination_match:
                            filtered_count += 1
                        else:
                            print(f"⚠️ Filtered out: {name} | Addr: {address}")
                            
                    print(f"Results after filtering: {filtered_count}")
            else:
                print(f"Error: {search_resp.text}")
        except Exception as e:
            print(f"Exception: {e}")

        # Try Method B: Bearer Header
        print("\n--- Method B: Bearer Header ---")
        try:
            search_resp = await client.get(
                search_url,
                params={
                    "query": query,
                    "region": "IND"
                },
                headers={"Authorization": f"Bearer {access_token}"}
            )
            print(f"Status: {search_resp.status_code}")
            if search_resp.status_code == 200:
                print("✅ Bearer Header works too/instead")
            else:
                print(f"❌ Bearer Header Failed: {search_resp.status_code}")
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_search())
