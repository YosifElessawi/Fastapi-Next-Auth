# Full-Stack Authentication Architecture (FastAPI + Next.js)

A production-ready, full-stack monorepo demonstrating robust software fundamentals, decoupled architecture, and advanced authentication patterns. Built with **FastAPI** (Python) on the backend and **Next.js 15** (TypeScript) on the frontend.

Designed to serve as a scalable foundation for enterprise applications, this project heavily emphasizes backend security, observability, and data integrity.

---

## 🏗️ Architecture & Fundamentals

Unlike rapid-prototyping templates, this repository focuses on **Software Engineering Fundamentals**:

*   **Decoupled Services:** Strict separation of concerns between the React hydration layer and the Python REST API.
*   **Secure Authentication:** Implements JWT-based stateless authentication with robust hashing (bcrypt), token expiration, and role-based access control (RBAC).
*   **Database Migrations:** Full ACID-compliant schema management using **Alembic** and SQLAlchemy 2.0.
*   **Asynchronous I/O:** Fully async DB calls using `asyncpg` and Redis caching for high-throughput capability.
*   **Rate Limiting & Security:** Integrated `fastapi-limiter` and CORS middleware to protect against brute-force and cross-origin attacks.

---

## 🛠️ Technology Stack

### Backend (Python)
*   **Framework:** FastAPI
*   **ORM / Database:** SQLAlchemy 2.0 (Async), PostgreSQL (`asyncpg`), Alembic
*   **Caching & Throttling:** Redis, `fastapi-limiter`
*   **Security:** PyJWT, `passlib[bcrypt]`, `python-jose`
*   **Code Quality:** `pytest`, `flake8`, `mypy`, `black`, `isort`

### Frontend (TypeScript)
*   **Framework:** Next.js 15 (App Router)
*   **UI Library:** React.js, TailwindCSS
*   **State / Auth Integration:** Secure HTTP-only cookies and React Context

---

## ⚙️ Getting Started

### 1. Database & Cache
This project relies on PostgreSQL and Redis. Ensure both are running either locally or via Docker.
```bash
# Example Docker run
docker run --name pg-db -e POSTGRES_PASSWORD=secret -d -p 5432:5432 postgres
docker run --name redis-cache -d -p 6379:6379 redis
```

### 2. Backend Setup
Navigate to the `backend/` directory and spin up the API:
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run initial migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload
```
*API Docs available at: `http://localhost:8000/docs`*

### 3. Frontend Setup
Navigate to the `frontend/` directory:
```bash
cd frontend
npm install
npm run dev
```
*Client available at: `http://localhost:3000`*

---

## 🔒 Security Posture
*   **Password Hashing:** Passwords are never stored in plaintext (Bcrypt with salt rounds).
*   **JWT:** Access and Refresh tokens are cryptographically signed.
*   **Validation:** Strict Pydantic models validate all incoming payloads to prevent SQL Injection and XSS formatting.
*   **Rate Limiting:** IP-based request throttling via Redis prevents credential stuffing.

## 🧪 Testing
The backend is fully unit-tested using `pytest`.
```bash
pytest --cov=app tests/
```
