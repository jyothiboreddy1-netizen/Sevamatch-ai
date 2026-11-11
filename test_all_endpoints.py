import asyncio
import httpx
from bson import ObjectId

BASE_URL = "http://127.0.0.1:8000"

async def run_tests():
    # We can use httpx.AsyncClient with ASGITransport to test directly against app without needing uvicorn running!
    from app.main import app, lifespan
    
    async with lifespan(app):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
            print("1. Testing /health...")
            r = await client.get("/health")
            assert r.status_code == 200, r.text
            assert r.json().get("database") == "connected"
            print("   -> OK: Database connected")

            # 2. Register a unique volunteer
            vol_email = f"testvol_{ObjectId()}@test.org"
            print(f"2. Registering volunteer {vol_email}...")
            r = await client.post("/api/auth/register", json={
                "name": "Arjun Sharma",
                "email": vol_email,
                "password": "password123",
                "role": "volunteer"
            })
            assert r.status_code == 200, r.text
            vol_token = r.json()["access_token"]
            vol_headers = {"Authorization": f"Bearer {vol_token}"}
            print("   -> OK: Volunteer registered & token issued")

            # 3. Save volunteer profile with coordinates (Coimbatore: 11.0168, 76.9558)
            print("3. Saving volunteer profile with coordinates...")
            r = await client.put("/api/profiles/volunteer/me", headers=vol_headers, json={
                "name": "Arjun Sharma",
                "headline": "Full-Stack Developer & Mentor",
                "skills": ["Python", "React", "Teaching"],
                "interests": ["Education", "Youth empowerment"],
                "availability": "4 hrs on weekends",
                "location": "Coimbatore, Tamil Nadu",
                "latitude": 11.0168,
                "longitude": 76.9558,
                "preferred_mode": "Hybrid",
                "experience": "3 years mentoring engineering students",
                "bio": "Passionate about using tech for good."
            })
            assert r.status_code == 200, r.text
            print("   -> OK: Volunteer profile saved with coordinates")

            # 4. Register a unique NGO
            ngo_email = f"testngo_{ObjectId()}@test.org"
            print(f"4. Registering NGO {ngo_email}...")
            r = await client.post("/api/auth/register", json={
                "name": "EmpowerNext Foundation",
                "email": ngo_email,
                "password": "password123",
                "role": "ngo"
            })
            assert r.status_code == 200, r.text
            ngo_token = r.json()["access_token"]
            ngo_headers = {"Authorization": f"Bearer {ngo_token}"}
            print("   -> OK: NGO registered & token issued")

            # 5. Save NGO profile
            print("5. Saving NGO profile...")
            r = await client.put("/api/profiles/ngo/me", headers=ngo_headers, json={
                "organization_name": "EmpowerNext Foundation",
                "mission": "Empowering youth through tech skills.",
                "description": "Grassroots foundation providing technical training.",
                "registration_number": "ENF-TN-2024-001",
                "location": "Coimbatore, Tamil Nadu",
                "latitude": 11.0180,
                "longitude": 76.9570,
                "contact_email": ngo_email,
                "contact_phone": "+91 9988776655",
                "activities": ["Coding Bootcamps", "Mentorship"],
                "verification_status": "pending"
            })
            assert r.status_code == 200, r.text
            print("   -> OK: NGO profile saved")

            # 6. Test NGO verification
            print("6. Verifying NGO via demo toggle...")
            r = await client.post("/api/ngo/verify-demo", headers=ngo_headers)
            assert r.status_code == 200, r.text
            assert r.json()["status"] == "verified"
            print("   -> OK: NGO verified")

            # 7. Create Opportunity as verified NGO
            print("7. Creating opportunity...")
            r = await client.post("/api/opportunities", headers=ngo_headers, json={
                "title": "Python & AI Student Mentor",
                "description": "Guide undergraduate students in Python and AI fundamentals.",
                "cause": "Education",
                "location": "Coimbatore · Hybrid",
                "mode": "hybrid",
                "hours_per_week": "4 hrs / week",
                "duration": "10 weeks",
                "skills": ["Python", "Teaching", "Mentoring"],
                "status": "published"
            })
            assert r.status_code == 200, r.text
            opp_id = r.json()["opportunity_id"]
            print(f"   -> OK: Opportunity created (ID: {opp_id})")

            # 8. Test Location Radius Endpoints with various radii
            print("8. Testing radius discovery...")
            # Nearby NGOs with radius_km
            r = await client.get("/api/nearby/ngos?radius_km=5", headers=vol_headers)
            assert r.status_code == 200, r.text
            print(f"   -> Nearby NGOs within 5 km: {r.json()['count']}")

            r = await client.get("/api/nearby/ngos?radius_km=50", headers=vol_headers)
            assert r.status_code == 200, r.text
            print(f"   -> Nearby NGOs within 50 km: {r.json()['count']}")
            assert r.json()["count"] > 0

            # Nearby Volunteers for NGO
            r = await client.get("/api/ngo/nearby-volunteers?radius_km=25", headers=ngo_headers)
            assert r.status_code == 200, r.text
            print(f"   -> Nearby Volunteers within 25 km: {r.json()['count']}")
            assert r.json()["count"] > 0

            # Recommended opportunities with custom radius
            r = await client.get("/api/opportunities/recommended?radius_km=50", headers=vol_headers)
            assert r.status_code == 200, r.text
            items = r.json()["items"]
            print(f"   -> Recommended opportunities: {len(items)}, top score: {items[0]['match_score']}%")
            assert len(items) > 0

            # 9. Test Application flow
            print("9. Applying to opportunity...")
            r = await client.post("/api/applications", headers=vol_headers, json={
                "opportunity_id": opp_id,
                "message": "I would love to help mentor students in Python!"
            })
            assert r.status_code == 200, r.text
            app_id = r.json()["application_id"]
            print(f"   -> OK: Application submitted (ID: {app_id})")

            # Test duplicate apply protection
            r = await client.post("/api/applications", headers=vol_headers, json={
                "opportunity_id": opp_id,
                "message": "Duplicate attempt"
            })
            assert r.status_code == 409, "Should reject duplicate application"
            print("   -> OK: Duplicate application correctly rejected (409)")

            # Check Volunteer's applications list
            r = await client.get("/api/applications/me", headers=vol_headers)
            assert r.status_code == 200, r.text
            my_apps = r.json()["items"]
            assert len(my_apps) >= 1
            assert my_apps[0]["title"] == "Python & AI Student Mentor"
            print(f"   -> OK: Volunteer application list enriched with title: '{my_apps[0]['title']}'")

            # Check NGO applicants inbox
            r = await client.get("/api/ngo/applicants", headers=ngo_headers)
            assert r.status_code == 200, r.text
            ngo_apps = r.json()["items"]
            assert len(ngo_apps) >= 1
            assert ngo_apps[0]["volunteer_name"] == "Arjun Sharma"
            print(f"   -> OK: NGO applicant inbox enriched with volunteer name: '{ngo_apps[0]['volunteer_name']}'")

            # NGO updates application status
            r = await client.patch(f"/api/applications/{app_id}/status", headers=ngo_headers, json={
                "status": "accepted"
            })
            assert r.status_code == 200, r.text
            print("   -> OK: Application status updated to 'accepted'")

            # 10. Check NGO's opportunities list
            r = await client.get("/api/ngo/opportunities", headers=ngo_headers)
            assert r.status_code == 200, r.text
            my_opps = r.json()["items"]
            assert len(my_opps) >= 1
            assert my_opps[0]["applicant_count"] >= 1
            print(f"   -> OK: NGO opportunities listed with applicant count: {my_opps[0]['applicant_count']}")

            # 11. Test AI Chat
            print("11. Testing AI Chat...")
            r = await client.post("/api/ai/chat", headers=vol_headers, json={
                "messages": [{"role": "user", "content": "I know Python and want to teach students."}],
                "purpose": "general"
            })
            assert r.status_code == 200, r.text
            print(f"   -> OK: AI chat response: {r.json()['reply'][:60]}...")

            # 12. Admin NGOs list
            r = await client.get("/api/admin/ngos", headers=vol_headers)
            assert r.status_code == 200, r.text
            assert r.json()["count"] > 0
            print(f"   -> OK: Admin NGOs count: {r.json()['count']}")

            print("\n🎉 ALL BACKEND ENDPOINTS AND LOGIC PASSED 100%!")

if __name__ == "__main__":
    asyncio.run(run_tests())

