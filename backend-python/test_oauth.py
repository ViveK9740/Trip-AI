import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def test_oauth():
    print("Testing Mappls OAuth Flow...")
    
    client_id = os.getenv("MAPPLS_CLIENT_ID")
    client_secret = os.getenv("MAPPLS_CLIENT_SECRET")
    
    print(f"Client ID present: {bool(client_id)}")
    print(f"Client Secret present: {bool(client_secret)}")
    
    if not client_id or not client_secret:
        print("❌ Missing credentials in .env")
        return

    token_url = "https://outpost.mappls.com/api/security/oauth/token"
    
    print(f"Requesting token from {token_url}...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                token_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": client_id,
                    "client_secret": client_secret
                },
                timeout=10.0
            )
            
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                token = data.get("access_token")
                print(f"✅ Success! Access Token received.")
                print(f"Token type: {data.get('token_type')}")
                print(f"Expires in: {data.get('expires_in')}")
            else:
                print(f"❌ Failed: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_oauth())
