import asyncio
from services.travel_api import travel_api

async def test_bengaluru_restaurants():
    print("Testing Bengaluru restaurant data...")
    restaurants = await travel_api.search_restaurants('Bengaluru')
    print(f"\nFound {len(restaurants)} restaurants for Bengaluru\n")
    
    if len(restaurants) > 0:
        print("First 15 restaurants:")
        for i, r in enumerate(restaurants[:15], 1):
            print(f"{i}. {r['name']} - {r.get('address', 'No address')}")
    else:
        print("WARNING: No restaurants found!")
    
    return restaurants

if __name__ == "__main__":
    restaurants = asyncio.run(test_bengaluru_restaurants())
