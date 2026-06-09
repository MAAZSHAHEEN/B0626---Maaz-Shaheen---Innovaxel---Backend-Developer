# 🎟️ Event Registration System API

A RESTful API built with **FastAPI** and **SQLite** for managing events and user registrations.
Built as a take-home assessment for **Innovaxel** by **Maaz Shaheen**.

---

## 🚀 Tech Stack

| Technology | Purpose |
|---|---|
| FastAPI | Web framework |
| SQLite | Database |
| SQLAlchemy | ORM |
| Pydantic | Data validation |
| Uvicorn | ASGI server |

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/MAAZSHAHEEN/B0626---Maaz-Shaheen---Innovaxel---Backend-Developer.git
cd B0626---Maaz-Shaheen---Innovaxel---Backend-Developer
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
uvicorn main:app --reload
```

### 5. Open Swagger UI
```
http://127.0.0.1:8000/docs
```

---

## 📌 API Endpoints

### Events
| Method | Endpoint | Description |
|---|---|---|
| POST | `/events` | Create a new event |
| GET | `/events` | Get all events (sorted by date) |
| GET | `/events?upcoming_only=true` | Get upcoming events only |

### Registrations
| Method | Endpoint | Description |
|---|---|---|
| POST | `/events/{event_id}/register` | Register a user for an event |
| DELETE | `/events/{event_id}/registrations/{registration_id}` | Cancel a registration |

---

## ✅ Features

- Create events with unique names, future dates and positive seat count
- Automatic available seat tracking
- Prevent overbooking with row-level locking (`with_for_update()`)
- Prevent duplicate registrations
- Soft delete for cancellations — data history preserved
- Filter upcoming events
- Full validation with proper HTTP status codes
- Interactive API docs via Swagger UI

---

## 🔒 Race Condition Prevention

This API handles concurrent registration requests using SQLAlchemy's `with_for_update()` which locks the event row during a transaction — preventing two users from booking the last seat simultaneously.

---

## 📁 Project Structure

```
B0626-Maaz-Shaheen-Innovaxel/
│
├── main.py              # Entry point
├── database.py          # Database connection & session
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic request/response schemas
├── requirements.txt     # Project dependencies
│
└── routers/
    ├── events.py        # Event endpoints
    └── registrations.py # Registration endpoints
```

---

## 👨‍💻 Author

**Maaz Shaheen**
Assessment for Backend Developer Position — Innovaxel

## 🌐 Live Demo

API is live at: https://b0626-maaz-shaheen-innovaxel.fastapicloud.dev

Interactive docs: https://b0626-maaz-shaheen-innovaxel.fastapicloud.dev/docs