import os
from dotenv import load_dotenv
from pymongo import MongoClient
from urllib.parse import quote_plus

load_dotenv()

# Get credentials
raw_url = os.getenv("MONGODB_URL")
print(f"Raw URL: {raw_url[:50]}...")

# Try different connection methods
print("\n=== Test 1: Direct connection with current URL ===")
try:
    client = MongoClient(raw_url, serverSelectionTimeoutMS=10000)
    client.admin.command('ping')
    print("✅ Connection successful!")
    client.close()
except Exception as e:
    print(f"❌ Error: {str(e)[:200]}")

print("\n=== Test 2: Connection with ssl=true parameter ===")
try:
    url_with_ssl = raw_url + "&ssl=true&ssl_cert_reqs=CERT_NONE"
    client = MongoClient(url_with_ssl, serverSelectionTimeoutMS=10000)
    client.admin.command('ping')
    print("✅ Connection successful!")
    client.close()
except Exception as e:
    print(f"❌ Error: {str(e)[:200]}")

print("\n=== Test 3: Connection with retryWrites=true ===")
try:
    url_retry = raw_url + "&retryWrites=true&w=majority"
    client = MongoClient(url_retry, serverSelectionTimeoutMS=10000)
    client.admin.command('ping')
    print("✅ Connection successful!")
    client.close()
except Exception as e:
    print(f"❌ Error: {str(e)[:200]}")

print("\n=== Test 4: Manual credential encoding ===")
try:
    username = "viveky9740_db_user"
    password = "Viveky@2901"
    host = "cluster0.rwdonui.mongodb.net"
    
    # URL encode password
    encoded_password = quote_plus(password)
    manual_url = f"mongodb+srv://{username}:{encoded_password}@{host}/?retryWrites=true&w=majority"
    
    print(f"Manual URL: mongodb+srv://{username}:***@{host}/...")
    client = MongoClient(manual_url, serverSelectionTimeoutMS=10000)
    client.admin.command('ping')
    print("✅ Connection successful!")
    
    # Try to access database
    db = client.tripai
    print(f"Database: {db.name}")
    print(f"Collections: {db.list_collection_names()}")
    
    client.close()
except Exception as e:
    print(f"❌ Error: {str(e)[:200]}")
    import traceback
    print("\nFull traceback:")
    traceback.print_exc()

print("\n=== Test 5: pymongo with certifi ===")
try:
    import certifi
    username = "viveky9740_db_user"
    password = quote_plus("Viveky@2901")
    host = "cluster0.rwdonui.mongodb.net"
    
    url = f"mongodb+srv://{username}:{password}@{host}/?retryWrites=true&w=majority"
    client = MongoClient(url, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=10000)
    client.admin.command('ping')
    print("✅ Connection successful with certifi!")
    client.close()
except Exception as e:
    print(f"❌ Error: {str(e)[:200]}")
