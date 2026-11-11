# SevaMatch AI — Full-Stack Platform

AI-powered volunteer & NGO matching platform built with **FastAPI**, **MongoDB**, and **React + Vite**.

---

## 🌟 What Is Implemented & Connected

### 1. Separate Workspaces & Authentication
- **Volunteer & NGO Auth**: Role-specific registration and login with JWT tokens (`/api/auth/register`, `/api/auth/login`, `/api/auth/me`).
- **Role Isolation**: Volunteer workspace and NGO workspace have dedicated navigation, tools, and capabilities.

### 2. Conversational Profile Onboarding & City Presets
- **Step-by-Step AI Chat**: Powered by `/api/ai/profile-preview` (OpenAI `gpt-4o-mini` with intelligent deterministic fallback).
- **Coordinate & Geolocation Helper**:
  - One-click **Use my current GPS location** via browser geolocation API.
  - Quick **City Coordinate Presets** (Coimbatore, Bengaluru, Chennai, Mumbai, Delhi, Hyderabad) to auto-fill latitude & longitude.
  - Manual numeric coordinate entry for custom coordinates.
- **Persistence**: Saved directly to MongoDB via `PUT /api/profiles/volunteer/me` and `PUT /api/profiles/ngo/me`.

### 3. Dynamic Location Radius Discovery (10 km – 200 km)
- **Configurable Radius Filter**: Interactive radius selector pills (`10 km`, `25 km`, `50 km`, `100 km`, `200 km`).
- **Endpoints**:
  - `GET /api/nearby/ngos?radius_km={r}`: Verified NGOs within radius.
  - `GET /api/ngo/nearby-volunteers?radius_km={r}`: Active volunteers within radius.
  - `GET /api/opportunities/recommended?radius_km={r}`: Filters opportunities within radius and calculates distance-weighted scores.
- **Distance Calculation**: Accurate spherical distances using the Haversine formula.

### 4. Semantic AI Matching Engine
- **Multi-Factor Scoring**: Weighted combination of:
  - 50% Semantic similarity (OpenAI `text-embedding-3-small` or local lexical fallback)
  - 25% Skills overlap
  - 15% Cause interest alignment
  - 10% Proximity / location score
- **Interactive Application**: Apply directly from the AI matches feed with personal notes.

### 5. Live AI Assistant (Chat)
- **Backend Connected**: Calls `POST /api/ai/chat` preserving multi-turn conversation context.
- **Context-Aware Responses**: Supports both OpenAI mode and smart local guidance for technical volunteering, tutoring, environmental causes, and location discovery.

### 6. Opportunity Publishing & Applicant Management (NGO Workspace)
- **Post an Opportunity**: Modal form for verified NGOs (`POST /api/opportunities`) with cause, mode (on-site, remote, hybrid), time commitment, and skill requirements.
- **My Opportunities View**: Lists published opportunities with live applicant counts (`GET /api/ngo/opportunities`).
- **Volunteer Applicants Inbox**: Dedicated screen (`GET /api/ngo/applicants`) showing volunteer profiles, skills, messages, and action buttons to **Accept**, **Review**, or **Decline** (`PATCH /api/applications/{id}/status`).
- **1-Click Demo Verification Toggle**: NGOs can toggle verification status (`POST /api/ngo/verify-demo`) to test opportunity publishing immediately without manual database edits.

### 7. Applications Tracking (Volunteer Workspace)
- **My Applications**: Real-time history loaded from MongoDB (`GET /api/applications/me`) with opportunity details and live status pills (`submitted`, `under_review`, `accepted`, `rejected`).
- **Duplicate Prevention**: Backend prevents duplicate applications with an HTTP 409 conflict.

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB running locally on `localhost:27017` or a MongoDB Atlas URI

### 1. Start MongoDB
Ensure MongoDB is running locally:
```bash
# Example with brew on macOS:
brew services start mongodb-community
```

### 2. Seed Initial Data (Optional but Recommended)
Populate verified sample NGOs, opportunities, and test accounts:
```bash
cd backend
.venv/bin/python seed_db.py
cd ..
```

### 3. Start Backend
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```
- API Docs: http://127.0.0.1:8000/docs
- Health Check: http://127.0.0.1:8000/health

### 4. Start Frontend
In a new terminal at the project root:
```bash
npm install
npm run dev
```
Open the Vite URL (typically http://localhost:5173).

---

## 🧪 Automated Testing
Run the backend test suite verifying all endpoints, location radius discovery, opportunity creation, and application flows:
```bash
cd backend
.venv/bin/python test_all_endpoints.py
```

---

## 📦 Production Deployment

### Frontend Production Build
```bash
npm run build
```
Generates optimized static assets in the `dist/` directory ready for deployment to Vercel, Netlify, Cloudflare Pages, or Nginx.

### Containerized Deployment (Docker Compose)
A `docker-compose.yml` and `backend/Dockerfile` are included:
```bash
docker-compose up --build
```
This starts MongoDB on port `27017` and the FastAPI backend on port `8000`.
