import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def test_mappls_oauth():
    client_id = os.getenv("MAPPLS_CLIENT_ID")
    client_secret = os.getenv("MAPPLS_CLIENT_SECRET")
    
    print(f"Client ID found: {'Yes' if client_id else 'No'}")
    print(f"Client Secret found: {'Yes' if client_secret else 'No'}")
    
    if not client_id or not client_secret:
        print("\n❌ Missing MAPPLS_CLIENT_ID or MAPPLS_CLIENT_SECRET in .env")
        print("You need BOTH values from Mappls API Console")
        return

    # Step 1: Generate Access Token
    token_url = "https://outpost.mappls.com/api/security/oauth/token"
    
    async with httpx.AsyncClient() as client:
        try:
            print("\n🔑 Requesting access token...")
            response = await client.post(
                token_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": client_id,
                    "client_secret": client_secret
                },
                timeout=10.0
            )
            
            print(f"Token Response Status: {response.status_code}")
            
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data.get("access_token")
                print(f"✅ Access Token obtained: {access_token[:20]}...")
                
                # Step 2: Test with the access token
                print("\n🌍 Testing place search with access token...")
                search_url = "https://atlas.mappls.com/api/places/search/json"
                
                search_response = await client.get(
                    search_url,
                    params={
                        "query": "restaurant in Indiranagar Bangalore",
                        "access_token": access_token
                    },
                    timeout=10.0
                )
                
                print(f"Search Status: {search_response.status_code}")
                if search_response.status_code == 200:
                    data = search_response.json()
                    results = data.get("suggestedLocations", [])
                    print(f"✅ Found {len(results)} places!")
                    if results:
                        print(f"First result: {results[0]}")
                else:
                    print(f"Search Error: {search_response.text}")
            else:
                print(f"❌ Token Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_mappls_oauth())
