# AstroHealth 🚀
### Astronaut Health Monitoring System

AstroHealth is a web-based astronaut health monitoring prototype developed for **NASA Space Apps Challenge 2026 – Challenge 4: Create Health Monitoring Software for Astronauts on Space Missions.**

The project aims to provide astronauts with a centralized platform to monitor their health metrics, review historical readings, receive health alerts, and interact with an AI-powered wellness assistant.

AstroHealth currently uses simulated health data to demonstrate the functionality of a real-time astronaut health monitoring system. It is designed with the possibility of future integration with wearable devices and health sensors.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Objectives](#objectives)
3. [Key Features](#key-features)
4. [Technology Stack](#technology-stack)
5. [System Architecture](#system-architecture)
6. [Project Structure](#project-structure)
7. [Health Monitoring](#health-monitoring)
8. [Real-Time Communication](#real-time-communication)
9. [Alert Management](#alert-management)
10. [AI Health Assistant](#ai-health-assistant)
11. [Authentication and Security](#authentication-and-security)
12. [Database Design](#database-design)
13. [API Endpoints](#api-endpoints)
14. [Installation and Setup](#installation-and-setup)
15. [Running the Application](#running-the-application)
16. [Environment Configuration](#environment-configuration)
17. [Current Limitations](#current-limitations)
18. [Future Improvements](#future-improvements)
19. [Disclaimer](#disclaimer)

---

## Project Overview

Astronauts operate in an environment where continuous health monitoring is important. Space missions can expose astronauts to conditions that affect cardiovascular health, oxygen levels, body temperature, physical activity, and sleep patterns.

AstroHealth provides a centralized dashboard where an astronaut can:

- View their latest health readings.
- Monitor changes in health metrics.
- Receive alerts when readings cross configured thresholds.
- Review historical health observations.
- Get general health explanations through an AI assistant.
- View and update their astronaut profile.

The application uses a React-based frontend, a FastAPI backend, a PostgreSQL database hosted through Supabase, and WebSockets for real-time communication.

## Objectives

The primary objectives of AstroHealth are:

- Provide an accessible astronaut health monitoring interface.
- Demonstrate real-time health data updates.
- Store and retrieve health observations securely.
- Identify potentially concerning readings through rule-based alerts.
- Provide AI-assisted explanations of health information.
- Establish a foundation for future wearable and sensor integration.

---

## Key Features

### 1. Personal Health Dashboard

The dashboard provides an overview of an astronaut's health information.

It includes:

- Latest health metric readings.
- Health status indicators.
- Historical health trends.
- Real-time connection status.
- Simulated health reading generation.
- Quick access to other application modules.

### 2. Health Monitoring

The health monitoring module handles different categories of health information.

Currently supported metrics include:

| Health Metric | Description |
|---|---|
| Heart Rate | Measures heartbeats per minute (BPM). |
| SpO2 | Measures peripheral blood oxygen saturation. |
| Body Temperature | Records body temperature. |
| Physical Activity | Tracks activity-related observations. |
| Sleep | Stores sleep-related observations. |

The system stores observations with timestamps, measurement units, data sources, and quality information.

### 3. Historical Health Trends

AstroHealth stores health observations and allows users to review historical data.

Charts help visualize changes in health readings over time.

### 4. Alert Management

The application uses rule-based logic to identify readings that cross configured thresholds.

Alerts contain:

- Alert category.
- Severity.
- Title and message.
- Recommended action.
- Creation timestamp.
- Current status.

Supported alert statuses:

- NEW
- ACKNOWLEDGED
- RESOLVED

### 5. AI Health Assistant

AstroHealth integrates Groq-hosted AI through the OpenAI-compatible API.

The assistant can:

- Explain available health readings.
- Answer questions about health metrics.
- Provide general wellness suggestions.
- Use the authenticated astronaut's latest available health readings as context.
- Mention whether readings are simulated, manually entered, or sensor-based.
- Explain when relevant information is unavailable.

The assistant is designed for general wellness information and does not provide medical diagnoses or prescriptions.

### 6. Responsive Interface

The frontend is designed to support:

- Desktop computers.
- Laptops.
- Tablets.
- Mobile devices.

The navigation sidebar supports collapsible desktop navigation and a mobile slide-out menu.

---

## Technology Stack

### Frontend

| Technology | Purpose |
|---|---|
| React | User interface development |
| Vite | Frontend development server and build tool |
| JavaScript | Application logic |
| Tailwind CSS v4 | Styling and responsive layouts |
| React Router | Client-side navigation |
| Axios | HTTP communication with backend |
| Supabase JS | Supabase integration |
| Lucide React | Interface icons |
| Recharts | Health data visualization |

### Backend

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | REST API development |
| SQLAlchemy | Database ORM |
| PostgreSQL | Relational database |
| Supabase | Hosted PostgreSQL and authentication |
| pg8000 | PostgreSQL database driver |
| Pydantic | Data validation |
| WebSockets | Real-time communication |
| OpenAI Python SDK | AI provider integration |
| Groq | AI inference provider |

---

## System Architecture

AstroHealth follows a frontend-backend architecture.

```text
                 ASTRONAUT
                     |
                     |
              REACT FRONTEND
                     |
          HTTP REST API / WebSocket
                     |
                     |
               FASTAPI BACKEND
                     |
          +----------+----------+
          |          |          |
          |          |          |
       AUTH       HEALTH       ALERTS
       MODULE     MODULE       MODULE
          |          |          |
          +----------+----------+
                     |
              SQLALCHEMY ORM
                     |
                     |
             SUPABASE POSTGRESQL
                     
                     
              AI HEALTH ASSISTANT
                     |
                GROQ API
                     |
                AI RESPONSE
                     |
               REACT FRONTEND
```

### Application Workflow

1. The astronaut registers or logs in.
2. Supabase authentication manages user authentication.
3. The frontend sends authenticated requests to FastAPI.
4. FastAPI validates the access token and identifies the astronaut.
5. Health observations are retrieved from PostgreSQL.
6. The frontend displays the available readings.
7. WebSockets deliver real-time health updates and new alerts.
8. The AI assistant receives the astronaut's latest available health context and generates a response.

---

## Project Structure

The project is organized into separate frontend and backend directories.

```text
AstroHealth/
│
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   └── config.py
│   │   │
│   │   ├── crud/
│   │   │   ├── astronaut.py
│   │   │   ├── health_metric.py
│   │   │   └── health_observation.py
│   │   │
│   │   ├── models/
│   │   │   ├── astronaut.py
│   │   │   ├── health_metric.py
│   │   │   └── health_observation.py
│   │   │
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── astronaut.py
│   │   │   ├── health.py
│   │   │   ├── alerts.py
│   │   │   ├── websocket.py
│   │   │   └── ai.py
│   │   │
│   │   ├── schemas/
│   │   ├── services/
│   │   │   ├── ai_service.py
│   │   │   └── websocket_service.py
│   │   │
│   │   ├── dependencies.py
│   │   ├── database.py
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── context/
│   │   ├── features/
│   │   ├── hooks/
│   │   ├── layouts/
│   │   ├── lib/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   ├── package-lock.json
│   └── .env.example
│
├── .gitignore
└── README.md
```

Note: This is a representative structure. Some folders may contain additional files as development progresses.

---

## Health Monitoring

Health observations are stored in the database and associated with the authenticated astronaut.

Each observation can contain:

- Metric identifier.
- Numeric or text value.
- Measurement unit.
- Observation timestamp.
- Data source.
- Measurement method.
- Quality status.
- Processing level.
- Additional metadata.

### Health Data Sources

The system supports the following data source classifications:

| Source | Description |
|---|---|
| SIMULATED | Generated data for development and demonstration. |
| MANUAL | Information entered manually. |
| SENSOR | Data originating from a connected sensor. |

The current implementation primarily uses simulated health observations.

### Data Quality

Health observations also include quality information, allowing the application to distinguish valid, suspect, and invalid observations.

This helps prevent invalid readings from being treated as reliable health information.

---

## Real-Time Communication

AstroHealth uses FastAPI WebSockets to provide real-time communication between the backend and frontend.

The WebSocket endpoint is:

```text
/ws/health
```

### Authentication

The frontend establishes a WebSocket connection and sends an authentication message containing the access token.

Example:

```json
{
  "type": "authenticate",
  "access_token": "YOUR_ACCESS_TOKEN"
}
```

### Real-Time Events

The system supports events such as:

- `connected` - Confirms successful connection.
- `health_update` - Sends updated health observations.
- `new_alert` - Notifies the frontend about a newly generated alert.

The frontend listens for these events and updates relevant dashboard information without requiring a full page reload.

---

## Alert Management

AstroHealth uses rule-based alert generation.

When a health observation meets a configured alert condition, the backend can generate an alert associated with the astronaut.

### Alert Lifecycle

```text
       NEW
        |
        v
  ACKNOWLEDGED
        |
        v
     RESOLVED
```

Users can review alerts, acknowledge them, and mark them as resolved.

Alert thresholds are application rules and should not be interpreted as a complete medical assessment.

---

## AI Health Assistant

The AI assistant provides conversational access to general health information.

### AI Integration

- Provider: Groq
- API compatibility: OpenAI-compatible API
- Model: `openai/gpt-oss-20b`
- Backend integration: OpenAI Python SDK

### How It Works

1. The astronaut submits a question through the frontend.
2. The backend identifies the authenticated astronaut.
3. The backend retrieves the astronaut's latest available health observations.
4. Relevant health information is prepared as context.
5. The context and question are sent to the Groq API.
6. The generated response is returned to the frontend.

### Example Questions

- What does my heart rate indicate?
- What are my latest health readings?
- How can I improve my sleep?
- What does my oxygen saturation reading mean?

The assistant is instructed not to invent missing readings, diagnose diseases, or prescribe medication.

---

## Authentication and Security

AstroHealth uses Supabase Authentication for user authentication.

### Authentication Features

- User registration.
- Email verification.
- User login.
- Access token validation.
- Refresh token rotation.
- Authenticated API requests.

### Backend Authentication

FastAPI verifies the supplied access token through Supabase and uses the authenticated user identity to retrieve the corresponding astronaut profile.

### Data Ownership

Health observations and alerts are associated with astronaut profiles.

Backend queries are scoped to the authenticated astronaut to prevent users from accessing another astronaut's private health records.

### Security Practices

- Environment variables are used for sensitive configuration.
- API requests use bearer-token authentication.
- Database credentials and API keys should never be committed to GitHub.
- CORS is configured for the frontend development origin.
- Authentication and authorization are handled on the backend.

---

## Database Design

AstroHealth uses PostgreSQL through Supabase.

Important database entities include:

| Entity | Responsibility |
|---|---|
| User Authentication | Stores and manages authentication identities through Supabase Auth. |
| Astronaut Profiles | Stores astronaut profile information and links it to the authenticated user. |
| Health Metrics | Defines available health metrics and their units. |
| Health Observations | Stores individual health readings. |
| Data Sources | Identifies where health data originates. |
| Alerts | Stores health-related alerts and their statuses. |

The backend uses SQLAlchemy to interact with PostgreSQL.

Existing database tables are managed through the established database schema rather than automatically recreating tables during application startup.

---

## API Endpoints

The backend exposes REST APIs through FastAPI.

Base URL:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/signup` | Register a new user. |
| POST | `/auth/login` | Authenticate a user. |
| POST | `/auth/refresh` | Refresh authentication tokens. |
| GET | `/auth/me` | Retrieve the authenticated user's information. |

### Astronaut Profile

| Method | Endpoint | Description |
|---|---|---|
| GET | `/astronaut/profile` | Retrieve the astronaut profile. |
| POST | `/astronaut/profile` | Create an astronaut profile. |
| PATCH | `/astronaut/profile` | Update profile information. |

### Health Monitoring

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health/metrics` | Retrieve available health metrics. |
| POST | `/health/observations` | Create a health observation. |
| GET | `/health/observations` | Retrieve health observation history. |
| GET | `/health/observations/{observation_id}` | Retrieve a specific observation. |
| POST | `/health/simulate` | Generate simulated health observations. |

### Alerts

| Method | Endpoint | Description |
|---|---|---|
| GET | `/alerts` | Retrieve astronaut alerts. |
| GET | `/alerts/{alert_id}` | Retrieve a specific alert. |
| PATCH | `/alerts/{alert_id}/status` | Update an alert status. |

### AI Assistant

| Method | Endpoint | Description |
|---|---|---|
| POST | `/ai/guidance` | Generate AI-powered health guidance. |

### WebSocket

| Type | Endpoint | Description |
|---|---|---|
| WebSocket | `/ws/health` | Real-time health updates and alerts. |

All protected endpoints require appropriate authentication.

---

## Installation and Setup

### Prerequisites

Install the following before running AstroHealth:

- Python 3.11 or a compatible supported Python version.
- Node.js and npm.
- Git.
- A Supabase project.
- A Groq API key.

### 1. Clone the Repository

```bash
git clone https://github.com/Muhammad-Hassaan9/Astro-Health-Hackathon-Project.git
```

Navigate to the project:

```bash
cd Astro-Health-Hackathon-Project
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

### 3. Backend Environment Configuration

Create a `.env` file inside the backend directory.

Configure the required environment variables according to `app/core/config.py`.

These include the database connection, Supabase authentication configuration, and Groq API key.

Do not commit the `.env` file.

### 4. Frontend Setup

Open another terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install frontend dependencies:

```bash
npm install
```

Configure frontend environment variables if required by the frontend configuration.

The frontend uses the local FastAPI backend by default:

```text
http://127.0.0.1:8000
```

---

## Running the Application

AstroHealth requires the backend and frontend development servers to run separately.

### Start the Backend

From the backend directory:

```bash
python -m uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

API Documentation:

```text
http://127.0.0.1:8000/docs
```

### Start the Frontend

From the frontend directory:

```bash
npm run dev
```

Frontend:

```text
http://localhost:5173
```

Open the frontend URL in your browser and register or log in to access the application.

### Production Frontend Build

To create a production build:

```bash
npm run build
```

The generated production files are placed in the frontend `dist` directory.

---

## Current Limitations

AstroHealth is currently a prototype developed for demonstration and hackathon purposes.

Current limitations include:

1. Health readings are primarily simulated rather than collected from actual astronaut wearable devices.
2. Real hardware and sensor integration has not yet been implemented.
3. AI-generated guidance is informational and is not a substitute for professional medical evaluation.
4. The alert system uses configured application rules and is not a certified medical alerting system.
5. The current interface focuses on the individual astronaut dashboard. A complete multi-astronaut Mission Control dashboard is a potential future enhancement.
6. Real mission deployment, space-qualified hardware integration, and validation in operational environments have not been performed.

---

## Future Improvements

Potential future development includes:

- Integration with wearable health monitoring devices.
- Real-time sensor data collection.
- Secure multi-astronaut Mission Control dashboard.
- Advanced health trend analysis.
- Improved anomaly detection.
- Historical health reports and analytics.
- More comprehensive sleep and physical activity monitoring.
- AI-assisted health trend summaries.
- Offline data handling and synchronization.
- Enhanced testing, deployment, and monitoring.

---

## Disclaimer

AstroHealth is an experimental software prototype created for the NASA Space Apps Challenge 2026.

It is not an official NASA product, certified medical device, or substitute for professional medical advice.

Health readings used in the current demonstration may be simulated. AI-generated responses are intended for general informational and wellness purposes only.

---

## Acknowledgements

Developed as a project for:

**NASA Space Apps Challenge 2026**

Challenge 4: Create Health Monitoring Software for Astronauts on Space Missions.

---

## License

No license has been specified yet. Unless a license is added to this repository, the project should be treated as having all rights reserved by its respective contributors.

---

**AstroHealth - Supporting Astronaut Health Through Technology.** 🚀
