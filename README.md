# 🌟 SevaMatch AI — Intelligent Volunteer & NGO Matching Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=flat&logo=react&logoColor=black)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-6.0+-646CFF?style=flat&logo=vite&logoColor=white)](https://vitejs.dev)
[![MongoDB](https://img.shields.io/badge/MongoDB-7.0+-47A248?style=flat&logo=mongodb&logoColor=white)](https://www.mongodb.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=flat&logo=openai&logoColor=white)](https://openai.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **SevaMatch AI** is a full-stack, AI-powered social impact platform that connects passionate volunteers with verified NGOs based on **semantic AI capability matching**, **dynamic location-radius discovery (10 km – 200 km)**, and **conversational profile onboarding**.

---

## 📌 Table of Contents
- [Architecture Overview](#-architecture-overview)
- [Key Features](#-key-features)
- [Technologies Used](#-technologies-used)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [1. Clone Repository](#1-clone-repository)
  - [2. Backend Setup](#2-backend-setup)
  - [3. Frontend Setup](#3-frontend-setup)
  - [4. Database Seeding](#4-database-seeding)
- [Running with Docker](#-running-with-docker)
- [1-Click Public Live Tunnel](#-1-click-public-live-tunnel)
- [Default Demo Credentials](#-default-demo-credentials)
- [API Endpoints Reference](#-api-endpoints-reference)
- [Matching Algorithm Breakdown](#-matching-algorithm-breakdown)
- [Testing & Quality Assurance](#-testing--quality-assurance)

---

## 🏗️ Architecture Overview

SevaMatch AI operates on a modern decoupled architecture where the FastAPI backend serves both the high-performance async REST API and the optimized single-page React frontend:

```
┌─────────────────────────────────────────────────────────────┐
│                       Client Browser                        │
│             React 18 + Vite + Lucide Icons (SPA)            │
└──────────────┬──────────────────────────────▲───────────────┘
               │ HTTP Requests                │ JSON Responses
               ▼                              │
┌─────────────────────────────────────────────────────────────┐
│                 FastAPI Async Application                   │
│                                                             │
│  ├── /api/auth/*       (JWT Authentication & RBAC)          │
│  ├── /api/ai/*         (LLM Chat & Profile Extraction)      │
│  ├── /api/nearby/*     (Haversine Spherical Geo-Filters)    │
│  ├── /api/opportunities (Semantic & Keyword Matching)       │
│  ├── /api/applications (Status Workflow & Review Inbox)     │
│  └── /api/admin/*      (NGO Verification Pipeline)          │
└──────────────┬──────────────────────────────┬───────────────┘
               │ Async PyMongo / Motor        │ Embeddings / Chat
               ▼                              ▼
┌──────────────────────────────┐ ┌────────────────────────────┐
│      MongoDB Database        │ │    OpenAI API Engine       │
│  ├── users                   │ │  ├── text-embedding-3-sm  │
│  ├── volunteer_profiles      │ │  ├── gpt-4o-mini           │
│  ├── ngo_profiles            │ │  └── (Smart Local Fallback)│
│  ├── opportunities           │ └────────────────────────────┘
│  └── applications            │
└──────────────────────────────┘
```

---

## ✨ Key Features

### 1. Dual Role-Specific Workspaces
- **Volunteer Workspace**:
  - **Overview**: Real-time stats, recommended opportunities, nearby verified NGOs, and active application counters.
  - **Explore Opportunities**: Search, cause filters (Education, Environment, Health, Animal Welfare, Community), and mode filters (On-site, Hybrid, Remote).
  - **AI Matches**: Semantic match scores calculated from user profile skills, causes, and proximity.
  - **AI Assistant**: Real-time interactive AI chat with context-aware social-good volunteering guidance.
  - **My Applications**: Live status tracking (`submitted`, `under_review`, `accepted`, `rejected`).
  - **My Profile**: Conversational AI profile builder with GPS & city coordinate presets.

- **NGO Workspace**:
  - **NGO Overview**: Quick stats, verification status pill, 1-click test verification toggle, and nearby volunteers feed.
  - **Post Opportunities**: Modal form for publishing roles with time commitment, cause, mode, and required skills.
  - **My Opportunities**: Listing management with real-time applicant counts.
  - **Volunteer Applicants Inbox**: Dedicated candidate assessment screen with 1-click actions: **Accept**, **Review**, or **Decline**.
  - **Organization Profile**: Mission, registration numbers, contact details, and location coordinates.

### 2. Conversational Profile Onboarding (Generative AI)
- Multi-step interactive Q&A assistant extracting skills, interests, availability, and experience into structured schemas using `gpt-4o-mini` function calling / JSON extraction.
- **Smart Local Fallback**: Seamlessly works offline or without API keys using deterministic heuristic extraction.

### 3. Dynamic Location-Radius Discovery (10 km – 200 km)
- Geolocation filtering using the **Haversine spherical distance formula**.
- Configurable radius filters (`10 km`, `25 km`, `50 km`, `100 km`, `200 km`).
- Pre-configured city coordinate presets (Coimbatore, Bengaluru, Chennai, Mumbai, Delhi, Hyderabad) or one-click browser GPS detection.

### 4. Semantic Multi-Factor AI Matching Engine
Opportunity ranking calculates a weighted composite score:
$$\text{Score} = (0.50 \times \text{Semantic Similarity}) + (0.25 \times \text{Skills Overlap}) + (0.15 \times \text{Cause Alignment}) + (0.10 \times \text{Proximity Score})$$

---

## 🛠️ Technologies Used

### Frontend
- **React 18**: Component-based UI with declarative reactive hooks (`useState`, `useEffect`, `useMemo`).
- **Vite 6**: Next-generation frontend tooling and ultra-fast HMR bundler.
- **Lucide React**: Modern, accessible icon library.
- **Custom CSS Design System**: Responsive, mobile-first design with accessible color contrast and typography.

### Backend
- **FastAPI**: Modern, high-performance web framework for Python based on standard type hints.
- **Motor**: Asynchronous Python driver for MongoDB powered by `asyncio`.
- **Pydantic v2**: Data validation and schema enforcement.
- **Uvicorn**: Lightning-fast ASGI web server implementation.
- **Pwdlib & Bcrypt**: Secure password hashing algorithms.
- **Python-JOSE**: JWT (JSON Web Token) creation, signing, and verification.

### Artificial Intelligence & Machine Learning
- **OpenAI API**:
  - `gpt-4o-mini`: Conversational AI chat assistant and structured profile extraction.
  - `text-embedding-3-small`: 1536-dimensional semantic embeddings for opportunity matching.
- **Intelligent Fallback Engine**: Local lexical overlap and cosine vector simulation ensuring 100% functionality without active external API billing.

### Database & Infrastructure
- **MongoDB 7.0**: Document-oriented NoSQL database with optimized multi-field compound indexes.
- **Cloudflare Tunnel (`cloudflared`)**: Secure edge tunneling providing public HTTPS live URLs without port-forwarding.
- **Docker & Docker Compose**: Containerized multi-service deployment setup.

---

## 📁 Project Structure

```bash
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── ai.py              # LLM chat, embeddings & local fallback engine
│   │   ├── config.py          # Pydantic environment configuration
│   │   ├── database.py        # MongoDB connection & index initialization
│   │   ├── main.py            # FastAPI routes, middleware & static file serving
│   │   ├── schemas.py         # Pydantic request/response models
│   │   └── security.py        # JWT generation, validation & role guard middleware
│   ├── .env.example           # Backend environment template
│   ├── Dockerfile             # Container definition for backend
│   ├── README.md              # Backend technical documentation
│   ├── requirements.txt       # Python dependencies
│   ├── seed_db.py             # Database seed script for test accounts
│   └── test_all_endpoints.py  # Automated integration test suite
├── src/
│   ├── App.jsx                # Main application component & views
│   ├── main.jsx               # React entry point
│   └── styles.css             # Unified modern CSS design system
├── index.html                 # HTML5 template
├── package.json               # Frontend dependencies & scripts
├── docker-compose.yml         # Container orchestration (MongoDB + Backend)
├── start_live.sh              # 1-click script to run server and Cloudflare tunnel
├── stop_live.sh               # 1-click script to stop background tunnel services
└── README.md                  # Complete project documentation
```

---

## 🚀 Getting Started

### Prerequisites
- **Node.js** (v18+) & **npm**
- **Python** (3.10+)
- **MongoDB** running locally on port 27017 or a **MongoDB Atlas URI**

### 1. Clone Repository
```bash
git clone https://github.com/jyothiboreddy1-netizen/GENAI-Project.git
cd GENAI-Project
```

### 2. Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env
```

Configure your `backend/.env` file:
```env
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=sevamatch
JWT_SECRET=your-secure-secret-key-here
JWT_EXPIRE_MINUTES=10080
OPENAI_API_KEY=               # Optional (Local AI fallback works automatically)
FRONTEND_ORIGINS=http://localhost:5173
```

### 3. Database Seeding
Populate initial verified NGOs, opportunities, and test accounts:
```bash
python seed_db.py
```

### 4. Frontend Setup
In the project root:
```bash
npm install
npm run dev
```
Open **http://localhost:5173** in your browser.

---

## 🐳 Running with Docker

Run the entire stack with a single command:
```bash
docker-compose up --build -d
```
Services initialized:
- **MongoDB**: `localhost:27017`
- **FastAPI Backend & Frontend**: `localhost:8000`

---

## 🌐 1-Click Public Live Tunnel

To expose your local instance to the web with an encrypted HTTPS link (accessible from mobile phones or external networks):

```bash
./start_live.sh
```
This builds the production assets, starts FastAPI, and provisions a Cloudflare Quick Tunnel.

To stop the tunnel:
```bash
./stop_live.sh
```

---

## 🔑 Default Demo Credentials

All test accounts seeded in `seed_db.py` share the password: **`password123`**

| Role | Name / Organization | Email | Features to Test |
|---|---|---|---|
| **Volunteer** | Jamie Doe | `volunteer@example.com` | AI matches, radius filtering, apply to roles, chat with AI |
| **NGO** | Bright Futures Foundation | `contact@brightfutures.org` | Post listings, review applicant inbox, 1-click verify |
| **NGO** | GreenRoots Collective | `team@greenroots.org` | Community gardening listings, applicant reviews |
| **NGO** | CareBridge NGO | `hello@carebridge.org` | Senior citizen digital literacy programs |

---

## 📡 API Endpoints Reference

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `POST` | `/api/auth/register` | Public | Register a volunteer or NGO account |
| `POST` | `/api/auth/login` | Public | Login and receive bearer JWT token |
| `GET` | `/api/auth/me` | User | Get current authenticated user details |
| `POST` | `/api/ai/chat` | User | Context-aware AI assistant reply |
| `POST` | `/api/ai/profile-preview` | User | Extract structured profile from Q&A |
| `GET` | `/api/profiles/me` | User | Fetch saved profile |
| `PUT` | `/api/profiles/volunteer/me` | Volunteer | Save volunteer profile with geolocation |
| `PUT` | `/api/profiles/ngo/me` | NGO | Save organization profile with geolocation |
| `POST` | `/api/ngo/verify-demo` | NGO | Toggle verification status for testing |
| `GET` | `/api/opportunities` | Public | Browse all opportunities with filters |
| `POST` | `/api/opportunities` | Verified NGO| Publish a new volunteer opportunity |
| `GET` | `/api/ngo/opportunities` | NGO | List own listings with applicant counts |
| `GET` | `/api/opportunities/recommended` | Volunteer | Semantic AI match feed with radius filter |
| `GET` | `/api/nearby/ngos` | Volunteer | Discover NGOs within `radius_km` |
| `GET` | `/api/ngo/nearby-volunteers` | NGO | Discover volunteers within `radius_km` |
| `POST` | `/api/applications` | Volunteer | Submit opportunity application |
| `GET` | `/api/applications/me` | Volunteer | Track user's submitted applications |
| `GET` | `/api/ngo/applicants` | NGO | Review incoming volunteer applications |
| `PATCH`| `/api/applications/{id}/status`| NGO | Update application status |
| `GET` | `/api/admin/ngos` | Admin | List all registered NGOs |
| `POST` | `/api/admin/ngos/{id}/verify`| Admin | Approve or reject NGO verification |

---

## 🧠 Matching Algorithm Breakdown

1. **Semantic Similarity (50%)**:
   - Vector cosine similarity between volunteer bio/skills and opportunity description using embeddings.
   - When offline, uses TF-IDF style lexical cosine overlap.
2. **Skills Overlap (25%)**:
   - Jaccard similarity index measuring exact and related skill matches.
3. **Cause Alignment (15%)**:
   - Compares volunteer's expressed causes with the opportunity's primary cause.
4. **Distance Proximity Score (10%)**:
   - Calculated using spherical distance:
     $$d = 2r \arcsin \left( \sqrt{\sin^2\left(\frac{\Delta\phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta\lambda}{2}\right)} \right)$$
   - Inverse exponential decay applied to rank closer opportunities higher within the chosen radius.

---

## 🧪 Testing & Quality Assurance

Run the automated integration test suite covering authentication, radius queries, opportunity publishing, and applicant review workflows:

```bash
cd backend
python test_all_endpoints.py
```

Expected output:
```
Testing SevaMatch AI Endpoints...
✓ Health & API Info Check
✓ Volunteer & NGO Registration
✓ Profile Updates with Geolocation
✓ Radius Discovery (10 km - 200 km)
✓ Opportunity Creation & Retrieval
✓ Application Submission & Duplicate Guards
✓ NGO Applicant Review & Status Updates
All integration tests completed successfully!
```

---

## 📄 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

