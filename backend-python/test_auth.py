import asyncio
import sys
from dotenv import load_dotenv

load_dotenv()

async def test_signup():
    try:
        print("Testing MongoDB connection...")
        from database.db import get_users_collection
        users = get_users_collection()
        print(f"✅ MongoDB connected. Collection: {users.name}")
        
        print("\nTesting password hashing...")
        from utils.auth import hash_password, verify_password
        password = "test123"
        hashed = hash_password(password)
        print(f"✅ Password hashed: {hashed[:20]}...")
        print(f"✅ Password verification: {verify_password(password, hashed)}")
        
        print("\nTesting user model...")
        from models.schemas import UserModel
        from datetime import datetime
        
        user_data = {
            "email": "test@example.com",
            "password_hash": hashed,
            "name": "Test User",
            "created_at": datetime.utcnow()
        }
        
        user = UserModel(**user_data)
        print(f"✅ User model created: {user.email}")
        
        user_dict = user.dict()
        print(f"✅ User dict: {user_dict.keys()}")
        
        print("\n✅ All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_signup())
