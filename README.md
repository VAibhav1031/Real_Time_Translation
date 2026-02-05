

# Doctor–Patient Real-Time Translation Web Application

## Overview

This project is a full-stack web application that acts as a real-time translation bridge between a doctor and a patient.
It is designed as a focused prototype to demonstrate system design, AI integration, and practical engineering trade-offs under time constraints.

The application supports a one-to-one doctor–patient conversation where messages (text) are automatically translated into the other participant’s language, logged for persistence, searchable, and summarizable using an LLM.

The goal of this project is t**clarity, correctness, and completeness**, not over-engineering things.

---

## Core Features Implemented

### 1. Doctor–Patient Roles

* Users explicitly join a conversation as either **Doctor** or **Patient**
* Both participants connect using a shared **Room ID**
* One room represents one conversation (1 doctor ↔ 1 patient)

### 2. Real-Time Translation (Text)

* Messages sent by one role are translated into the selected language of the other role
* Translation direction is deterministic and role-based
* Implemented using the **Google Gemini API (free tier)**

### 3. Chat Interface

* Clean, minimal UI built with server-rendered HTML (Jinja)
* Messages are visually differentiated:

  * Doctor messages aligned to the right
  * Patient messages aligned to the left
* Near real-time updates using polling

### 4. Conversation Logging

* All messages are stored in the database with:

  * room ID
  * role
  * original text
  * translated text
  * timestamp
* Conversation history persists beyond the active session

### 5. Conversation Summary (AI-Powered)

* A “Generate Summary” button produces a structured medical summary
* The summary highlights:

  * Symptoms
  * Diagnosis / Clinical Impression
  * Medications / Treatment
  * Follow-up instructions
* Generated using Gemini with a constrained, non-hallucinating prompt

### 6. Create Room / Join Room Flow

* Users can either:

  * **Create a room** (random room ID generated client-side)
  * **Join an existing room** using a shared ID
* The UX clearly separates these two actions to avoid confusion

### 7. Translation Caching

* A simple in-memory cache is used to avoid repeated LLM calls for identical translations
* Cache key includes:

  * source language
  * target language
  * message text
* This significantly reduces API usage and rate-limit pressure

---

## Tech Stack

### Backend

* **Python**
* **Flask**
* **Flask-WTF** (forms & CSRF handling)
* **SQLAlchemy**
* **Alembic** (migrations)
* **SQLite / Postgres** (environment-dependent)

### Frontend

* Server-rendered HTML (Jinja)
* Vanilla JavaScript
* Custom CSS (no frameworks)

### AI / LLM

* **Google Gemini API (free tier)**
* Used for:

  * translation
  * medical conversation summarization

### Tooling

* Docker
* docker-compose
* Environment-based configuration (dev / prod)

---

## Project Structure

```
.
├── Dockerfile
├── docker-compose.yaml
├── run.py
├── pyproject.toml
├── README.md
├── migrations/
├── rt_app/
│   ├── backend.py          # Routes and request handling
│   ├── config.py           # Environment-based configuration
│   ├── forms.py            # Flask-WTF forms
│   ├── gemini_service.py   # Gemini API integration
│   ├── models.py           # Database models
│   ├── templates/
│   │   ├── layout.html
│   │   ├── home.html
│   │   └── chat.html
```

---

## How the System Works (High Level)

1. A user creates or joins a room and selects:

   * role (doctor / patient)
   * their language
2. Room metadata (role + language) is stored once per participant
3. Messages are sent to the backend via JSON
4. The backend:

   * determines translation direction based on role
   * checks the translation cache
   * calls Gemini only if needed
   * stores both original and translated text
5. Clients poll for messages every few seconds
6. At any point, the conversation can be summarized using an LLM prompt

---

## Configuration & Environments

The app uses a **config-class based setup** to switch environments cleanly.

* Development
* Production

Configuration includes:

* database URL
* debug mode
* secret keys
* API keys

Environment variables control which config is active, allowing easy switching without code changes.

---

## Design Decisions & Trade-offs

### Polling instead of WebSockets

* Simpler and more reliable under time constraints
* Sufficient for low-volume, one-to-one chat
* Easier to reason about and debug

### No Authentication

* Out of scope for the assignment
* Focus was kept on translation, logging, and summarization
* Roles are explicit per session

### One Room = One Doctor + One Patient

* Avoids unnecessary complexity
* Matches the assignment’s core intent
* Easy to extend later

### In-Memory Translation Cache

* Reduces LLM usage and API limits
* Keeps the system simple
* Acceptable for a prototype (cache resets on restart)

---

## Known Limitations

* Audio recording UI is not implemented
* No user authentication or authorization
* Polling is not optimal for high-scale real-time systems
* In-memory cache is not persistent
* Only one conversation per room

These were **intentional trade-offs** to prioritize correctness, clarity, and timely delivery.

---

## What Could Be Added Next

If given more time:

* Audio recording and playback using MediaRecorder API
* WebSocket-based real-time messaging
* Persistent translation cache (Redis or DB)
* Multi-room support
* Authentication and access control
* Better error handling and retries for LLM calls

---

## AI Usage Disclosure

AI tools were used appropriately:

* Gemini API for translation and summarization
* LLM prompts were explicitly constrained to avoid hallucinations
* No model training or fine-tuning was performed

---

## Final Notes

This project intentionally focuses on **engineering judgment**:

* clear boundaries
* explicit trade-offs
* readable code
* working deployment

I Know It is not to be a production healthcare system, but a practical demonstration of how such a system could be designed and built responsibly under limited time.
Not good on frontend part, but can understand and love to work as a backend :)

