"""
Database Reset Script for SevaMatch AI.
Completely clears all collections (users, profiles, opportunities, applications)
and rebuilds the necessary unique and compound indexes.
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URI = "mongodb://localhost:27017"
DATABASE_NAME = "sevamatch"

async def clear_database():
    print(f"Connecting to MongoDB at {MONGODB_URI}...")
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DATABASE_NAME]

    collections = ["users", "volunteer_profiles", "ngo_profiles", "opportunities", "applications"]
    
    print(f"Clearing collections in '{DATABASE_NAME}'...")
    for coll_name in collections:
        result = await db[coll_name].delete_many({})
        print(f" - Cleared '{coll_name}': {result.deleted_count} documents removed.")

    print("\nRebuilding database indexes...")
    await db.users.create_index("email", unique=True)
    await db.volunteer_profiles.create_index("user_id", unique=True)
    await db.ngo_profiles.create_index("user_id", unique=True)
    await db.opportunities.create_index([("status", 1), ("created_at", -1)])
    await db.applications.create_index([("volunteer_id", 1), ("opportunity_id", 1)], unique=True)
    print("✓ All indexes verified and recreated.")

    print("\n==========================================")
    print(f"Database '{DATABASE_NAME}' is now 100% clean and ready for fresh registrations.")
    print("==========================================")
    client.close()

if __name__ == "__main__":
    asyncio.run(clear_database())

