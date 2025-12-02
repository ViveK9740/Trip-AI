from pymongo import MongoClient
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    client: Optional[MongoClient] = None
    db = None

def get_database():
    """Get MongoDB database instance"""
    if Database.client is None:
        mongodb_url = os.getenv("MONGODB_URL")
        if not mongodb_url:
            raise ValueError("MONGODB_URL not found in environment variables")
        
        try:
            # Connect with longer timeout for stability
            Database.client = MongoClient(
                mongodb_url, 
                serverSelectionTimeoutMS=20000,
                connectTimeoutMS=20000
            )
            # Test the connection
            Database.client.admin.command('ping')
            Database.db = Database.client.tripai
            
            # Create indexes
            Database.db.users.create_index("email", unique=True)
            Database.db.trips.create_index("user_id")
            
            print("✅ Connected to MongoDB Atlas")
        except Exception as e:
            print(f"❌ MongoDB Connection Error: {str(e)}")
            raise
    
    return Database.db

def close_database():
    """Close MongoDB connection"""
    if Database.client:
        Database.client.close()
        Database.client = None
        Database.db = None
        print("🔌 MongoDB connection closed")

# Collections
def get_users_collection():
    db = get_database()
    return db.users

def get_trips_collection():
    db = get_database()
    return db.trips
