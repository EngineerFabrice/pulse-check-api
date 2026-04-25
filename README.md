#  Pulse Check API (Watchdog Sentinel)

A **Dead Man’s Switch Monitoring System** built with FastAPI that tracks remote devices and automatically triggers alerts when they stop sending heartbeats.

This project simulates a real-world **FinTech / Infrastructure Monitoring system** used to detect device failures in real time.

---

#  Problem Statement

Remote devices (solar farms, sensors, weather stations) must send periodic heartbeats.

If a device stops responding:
- The system must detect failure
- Trigger an alert automatically
- Notify support engineers immediately

---

# 🧠 Core Concept

Each device has a **monitor with a countdown timer**:

- When heartbeat is received → timer resets
- When timer reaches zero → alert is triggered
- If paused → no alerts fire
- If resumed → monitoring continues

---

# 🏗️ Architecture


Client Device
↓
FastAPI Layer (Routes)
↓
Service Layer (Business Logic)
↓
State Layer (In-memory Store)
↓
Scheduler / Worker (Timer Engine)
↓
Alert Service (Notification System)


📊 Architecture Diagram:
![Architecture](docs/architecture.png)

---

# ⚙️ Features

## Core Features
- Device monitor registration (`/monitors`)
- Heartbeat reset system (`/monitors/{id}/heartbeat`)
- Automatic countdown timer
- Dead-man switch detection
- Pause / Resume monitoring system

## Advanced Features
- Async background worker
- In-memory state store
- Thread-safe timer scheduler
- Structured logging system

---

# 📡 API Documentation

## 1. Register Monitor

### `POST /monitors`

```json
{
  "id": "device-123",
  "timeout": 60,
  "alert_email": "admin@critmon.com"
}
Response
{
  "message": "Monitor created successfully"
}
2. Heartbeat
POST /monitors/{id}/heartbeat
Response
{
  "message": "Heartbeat received, timer reset"
}
3. Pause Monitor
POST /monitors/{id}/pause
Response
{
  "message": "Monitor paused"
}
4. Alert Output (System Trigger)

When device fails:

{
  "ALERT": "Device device-123 is down!",
  "time": "2026-04-25T12:00:00Z"
}
⚙️ Setup Instructions
1. Clone Repository
git clone https://github.com/EngineerFabrice/pulse-check-api.git
cd pulse-check-api
2. Create Virtual Environment
python -m venv .venv
.venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Run Server
uvicorn app.main:app --reload
5. Open API Docs
http://127.0.0.1:8000/docs
🧠 Design Decisions
1. In-Memory Store

Used for fast access and simplicity. Can be replaced with Redis for production scaling.

2. Async Scheduler

Handles countdown timers without blocking the API.

3. Separation of Concerns
API → request handling
Services → business logic
State → memory storage
Workers → background processing
4. Thread-Safe Design

Prevents race conditions when multiple heartbeats arrive.

⭐ Developer’s Choice Feature
🔁 Retry Alert System (Implemented Bonus Feature)
Problem:

If a device remains offline, a single alert is not enough.

Solution:

Implemented automatic retry alerts:

If device stays down
System re-triggers alert after interval
Prevents missed critical failures
Why this matters:

✔ Improves reliability
✔ Ensures alert delivery
✔ Prevents silent system failure
✔ Mimics real-world monitoring tools (Datadog / PagerDuty style)

🧪 Testing Flow
Register monitor
Send heartbeat → resets timer
Stop heartbeat → timer expires
Alert is triggered
Retry alert fires if device stays down
📁 Project Structure

app/
├── api/
├── core/
├── models/
├── schemas/
├── services/
├── state/
├── utils/
├── workers/

tests/

🚀 Tech Stack
Python 3.10+
FastAPI
Uvicorn
AsyncIO
📌 Author

Fabrice Ndayisaba
Computer & Software Engineering Student