"""
Seed script to create and initialize the MongoDB database 'sevamatch'.
Creates collections, builds required indexes, and populates initial sample data
(verified NGOs, published opportunities, demo volunteer, and test accounts).
"""
import asyncio
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from pwdlib import PasswordHash

pwd_hash = PasswordHash.recommended()

MONGODB_URI = "mongodb://localhost:27017"
DATABASE_NAME = "sevamatch"

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def hash_pw(password: str) -> str:
    return pwd_hash.hash(password)

async def init_database():
    print(f"Connecting to MongoDB at {MONGODB_URI}...")
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DATABASE_NAME]

    # Test connection
    await db.command("ping")
    print(f"Successfully connected to MongoDB server. Initializing database '{DATABASE_NAME}'...")

    # 1. Create indexes (as specified in backend/app/database.py)
    print("Creating indexes on collections...")
    await db.users.create_index("email", unique=True)
    await db.volunteer_profiles.create_index("user_id", unique=True)
    await db.ngo_profiles.create_index("user_id", unique=True)
    await db.opportunities.create_index([("status", 1), ("created_at", -1)])
    await db.applications.create_index([("volunteer_id", 1), ("opportunity_id", 1)], unique=True)
    print("Indexes created successfully.")

    # 2. Check if already seeded
    existing_users = await db.users.count_documents({})
    if existing_users > 0:
        print(f"Database '{DATABASE_NAME}' already contains {existing_users} users.")
        user_list = await db.users.find({}, {"email": 1, "role": 1, "name": 1}).to_list(100)
        print("Existing accounts:")
        for u in user_list:
            print(f" - {u.get('name')} ({u.get('email')}): {u.get('role')}")
        opp_count = await db.opportunities.count_documents({})
        print(f"Total published/existing opportunities: {opp_count}")
        return

    print("Seeding initial accounts, profiles, and opportunities...")

    # 3. Create Sample NGO Accounts & Verified Profiles
    sample_ngos = [
        {
            "name": "Bright Futures Foundation",
            "email": "contact@brightfutures.org",
            "password": hash_pw("password123"),
            "role": "ngo",
            "profile": {
                "organization_name": "Bright Futures Foundation",
                "mission": "Empowering underprivileged children through digital literacy and quality education.",
                "description": "We run weekend learning camps and coding clubs for school students across the region.",
                "registration_number": "BFF-EDU-2021-9871",
                "location": "Coimbatore, Tamil Nadu",
                "latitude": 11.0168,
                "longitude": 76.9558,
                "contact_email": "contact@brightfutures.org",
                "contact_phone": "+91 98765 43210",
                "activities": ["Coding clubs", "Mentorship", "Book drives", "School tutoring"],
                "verification_status": "verified"
            },
            "opportunities": [
                {
                    "title": "Weekend Coding Mentor",
                    "description": "Help school students discover the basics of programming through fun, beginner-friendly weekend sessions in Python and Scratch.",
                    "cause": "Education",
                    "location": "Coimbatore · Hybrid",
                    "mode": "hybrid",
                    "hours_per_week": "4 hrs / week",
                    "duration": "8 weeks",
                    "skills": ["Python", "Teaching", "Communication", "Scratch"],
                    "status": "published"
                }
            ]
        },
        {
            "name": "GreenRoots Collective",
            "email": "team@greenroots.org",
            "password": hash_pw("password123"),
            "role": "ngo",
            "profile": {
                "organization_name": "GreenRoots Collective",
                "mission": "Building resilient, eco-friendly urban communities through community gardening and waste management.",
                "description": "Grassroots community organization running urban micro-forests, seed banks, and local composting hubs.",
                "registration_number": "GRC-ENV-2022-4412",
                "location": "Coimbatore, Tamil Nadu",
                "latitude": 11.0200,
                "longitude": 76.9600,
                "contact_email": "team@greenroots.org",
                "contact_phone": "+91 94432 11223",
                "activities": ["Tree planting", "Urban gardening", "Composting workshops", "Zero waste drives"],
                "verification_status": "verified"
            },
            "opportunities": [
                {
                    "title": "Community Garden Volunteer",
                    "description": "Support neighbourhood gardening, organic composting and environmental awareness activities every weekend.",
                    "cause": "Environment",
                    "location": "Coimbatore · On-site",
                    "mode": "on-site",
                    "hours_per_week": "3 hrs / week",
                    "duration": "Ongoing",
                    "skills": ["Teamwork", "Gardening", "Community", "Composting"],
                    "status": "published"
                }
            ]
        },
        {
            "name": "CareBridge NGO",
            "email": "hello@carebridge.org",
            "password": hash_pw("password123"),
            "role": "ngo",
            "profile": {
                "organization_name": "CareBridge NGO",
                "mission": "Bridging digital and economic divides for senior citizens and marginalized community members.",
                "description": "Conducts weekly adult literacy and digital empowerment bootcamps.",
                "registration_number": "CBN-SOC-2020-5561",
                "location": "Coimbatore, Tamil Nadu",
                "latitude": 11.0050,
                "longitude": 76.9700,
                "contact_email": "hello@carebridge.org",
                "contact_phone": "+91 98421 99887",
                "activities": ["Senior citizen care", "Digital literacy", "Community healthcare"],
                "verification_status": "verified"
            },
            "opportunities": [
                {
                    "title": "Digital Skills Support",
                    "description": "Create simple digital step-by-step guides and support elders and community members learning essential smartphone and online banking skills.",
                    "cause": "Community",
                    "location": "Coimbatore · Flexible",
                    "mode": "hybrid",
                    "hours_per_week": "2–3 hrs / week",
                    "duration": "6 weeks",
                    "skills": ["Digital Literacy", "Excel", "Patience", "Communication"],
                    "status": "published"
                }
            ]
        },
        {
            "name": "Little Steps Initiative",
            "email": "info@littlesteps.org",
            "password": hash_pw("password123"),
            "role": "ngo",
            "profile": {
                "organization_name": "Little Steps Initiative",
                "mission": "Ensuring every child develops foundational literacy and reading confidence through dedicated learning buddies.",
                "description": "After-school reading and mentoring program for primary school children.",
                "registration_number": "LSI-EDU-2023-1109",
                "location": "Coimbatore, Tamil Nadu",
                "latitude": 11.0120,
                "longitude": 76.9500,
                "contact_email": "info@littlesteps.org",
                "contact_phone": "+91 97890 12345",
                "activities": ["Child education", "Reading clubs", "Storytelling sessions"],
                "verification_status": "verified"
            },
            "opportunities": [
                {
                    "title": "Learning Buddy for Children",
                    "description": "Spend quality time with children, read storybooks together and help them build confidence with their English and foundational math studies.",
                    "cause": "Education",
                    "location": "Coimbatore · On-site",
                    "mode": "on-site",
                    "hours_per_week": "2 hrs / week",
                    "duration": "12 weeks",
                    "skills": ["Mentoring", "English", "Teaching", "Empathy"],
                    "status": "published"
                }
            ]
        }
    ]

    for ngo_data in sample_ngos:
        # Create user
        user_doc = {
            "name": ngo_data["name"],
            "email": ngo_data["email"],
            "password_hash": ngo_data["password"],
            "role": ngo_data["role"],
            "created_at": now_iso()
        }
        res = await db.users.insert_one(user_doc)
        ngo_user_id = str(res.inserted_id)

        # Create NGO Profile
        profile_doc = ngo_data["profile"]
        profile_doc.update({
            "user_id": ngo_user_id,
            "created_at": now_iso(),
            "updated_at": now_iso(),
            "created_by_ai": False
        })
        await db.ngo_profiles.insert_one(profile_doc)

        # Create Opportunities
        for opp in ngo_data["opportunities"]:
            opp_doc = {
                **opp,
                "ngo_user_id": ngo_user_id,
                "ngo_name": ngo_data["profile"]["organization_name"],
                "created_at": now_iso(),
                "updated_at": now_iso()
            }
            await db.opportunities.insert_one(opp_doc)
            print(f"Created opportunity: '{opp['title']}' for {ngo_data['name']}")

    # 4. Create Sample Volunteer Account & Profile
    sample_volunteer = {
        "name": "Jamie Doe",
        "email": "volunteer@example.com",
        "password": hash_pw("password123"),
        "role": "volunteer",
        "profile": {
            "name": "Jamie Doe",
            "headline": "BTech Computer Science Student & Tech Enthusiast",
            "skills": ["Python", "Teaching", "Communication", "Digital Literacy", "Teamwork"],
            "interests": ["Education", "Environment", "Community"],
            "availability": "4 hours on weekends",
            "location": "Coimbatore, Tamil Nadu",
            "latitude": 11.0168,
            "longitude": 76.9558,
            "preferred_mode": "Hybrid",
            "experience": "Taught basic computer literacy to neighborhood kids and organized campus recycling drives.",
            "bio": "Passionate about using technology to uplift communities and mentor young learners in programming.",
            "created_at": now_iso(),
            "updated_at": now_iso(),
            "created_by_ai": True
        }
    }

    vol_user = {
        "name": sample_volunteer["name"],
        "email": sample_volunteer["email"],
        "password_hash": sample_volunteer["password"],
        "role": sample_volunteer["role"],
        "created_at": now_iso()
    }
    vol_res = await db.users.insert_one(vol_user)
    vol_user_id = str(vol_res.inserted_id)

    vol_profile = sample_volunteer["profile"]
    vol_profile["user_id"] = vol_user_id
    await db.volunteer_profiles.insert_one(vol_profile)
    print(f"Created demo volunteer account: '{sample_volunteer['email']}' (password: password123)")

    # Summary
    print("\n==========================================")
    print(f"MongoDB database '{DATABASE_NAME}' successfully initialized!")
    print(f" - Users: {await db.users.count_documents({})}")
    print(f" - NGO Profiles: {await db.ngo_profiles.count_documents({})}")
    print(f" - Volunteer Profiles: {await db.volunteer_profiles.count_documents({})}")
    print(f" - Opportunities: {await db.opportunities.count_documents({})}")
    print("==========================================")
    client.close()

if __name__ == "__main__":
    asyncio.run(init_database())
