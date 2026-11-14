# 🚀 AstroHealth — Astronaut Health Monitoring System

AstroHealth is a web-based astronaut health monitoring system designed to monitor health indicators, identify unusual changes, generate alerts, and provide AI-powered health explanations and general well-being suggestions.

The project aims to demonstrate how technology can support astronaut health monitoring during space missions through real-time data simulation, interactive visualizations, and AI assistance.

> **Project Status:** Under Development  
> **Project Type:** Web Application  
> **Project Category:** Space Health Monitoring & AI

---

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Problem Statement](#-problem-statement)
- [Project Objectives](#-project-objectives)
- [Key Features](#-key-features)
- [Health Indicators](#-health-indicators)
- [Technology Stack](#-technology-stack)
- [System Architecture](#-system-architecture)
- [Project Structure](#-project-structure)
- [Data Management](#-data-management)
- [Application Workflow](#-application-workflow)
- [Security and Privacy](#-security-and-privacy)
- [Project Limitations](#-project-limitations)
- [Future Goals](#-future-goals)
- [Installation and Setup](#-installation-and-setup)
- [Team and Contributions](#-team-and-contributions)

---

## 🌌 Project Overview

Astronauts experience several physical and psychological challenges during space missions, including microgravity, space radiation, isolation, sleep disturbances, and changes in cardiovascular and other body systems.

Monitoring these changes is important for understanding astronaut health and supporting their well-being during missions.

AstroHealth aims to provide a centralized personal health monitoring experience for an astronaut through a web application.

The system will use simulated health readings to demonstrate real-time monitoring, display health trends, generate alerts, and provide AI-powered explanations and general health suggestions.

The application will initially focus on an individual astronaut's personal dashboard.

---

## ⚠️ Problem Statement

Space missions expose astronauts to environments that can affect their physical and psychological health.

Traditional health monitoring approaches may not always provide an easily accessible, continuously updated overview of an astronaut's health information.

AstroHealth aims to address this challenge by providing:

- A personal health monitoring dashboard.
- Real-time updates of health indicators.
- Visual representation of health trends.
- Alerts for unusual health readings.
- AI-powered explanations and general well-being guidance.

---

## 🎯 Project Objectives

The main objectives of AstroHealth are:

1. To demonstrate real-time astronaut health monitoring.
2. To simulate health readings for demonstration purposes.
3. To visualize health indicators and historical trends.
4. To identify unusual readings and generate alerts.
5. To integrate an AI assistant for health-related explanations and general suggestions.
6. To provide a simple and accessible astronaut dashboard.
7. To explore how software technologies can support human health monitoring during space missions.

---

## ✨ Key Features

The following features are planned for the initial prototype.

### 1. User Authentication

- Secure user login.
- Individual astronaut accounts.
- Authentication through Supabase Auth.
- Protected access to personal health information.

### 2. Personal Health Dashboard

A dedicated dashboard where an astronaut can view their own health information.

It will include:

- Current health indicators.
- Health status overview.
- Recent readings.
- Health alerts.
- Historical health trends.

### 3. Real-Time Health Monitoring

The system will generate simulated health readings at regular intervals.

- Continuous updates during an active demo session.
- Real-time communication using FastAPI WebSockets.
- Automatic dashboard updates without manually refreshing the page.

### 4. Health Alerts

The system will analyze incoming readings using predefined prototype rules.

It will generate three types of health statuses:

- **Normal:** Readings are within the configured prototype range.
- **Warning:** A reading requires attention.
- **Critical:** A reading has crossed a configured critical threshold.

Alerts will help demonstrate how unusual health changes can be identified.

### 5. Health History and Visualization

- Historical health readings.
- Interactive graphs and charts.
- Health indicator trends.
- Changes in readings over time.

### 6. AI Health Assistant

An AI-powered assistant integrated through the Google Gemini API.

It will help users:

- Understand their health readings.
- Understand why an alert was generated.
- Receive general health and well-being suggestions.
- Ask questions related to astronaut health and spaceflight challenges.

The project will use an existing pre-trained AI model. No custom AI model training or fine-tuning is planned for the initial prototype.

---

## ❤️ Health Indicators

The initial prototype will focus on the following indicators:

| Indicator | Purpose | Data Source |
|---|---|---|
| Heart Rate | Monitor heart rate changes | Simulated |
| SpO₂ | Demonstrate blood oxygen monitoring | Simulated |
| Body Temperature | Monitor temperature changes | Simulated |
| Physical Activity | Track activity levels | Simulated |
| Sleep | Demonstrate sleep duration and patterns | Simulated |
| Mood / Well-being | Represent self-reported psychological well-being | Simulated / User Input |

These indicators are selected to demonstrate different aspects of astronaut health monitoring.

The thresholds used for prototype alerts will be clearly identified as demonstration rules and not presented as NASA-approved medical limits.

---

## 🛠️ Technology Stack

The following technologies are selected for developing AstroHealth.

### Frontend

| Technology | Purpose |
|---|---|
| React.js | Building the user interface |
| Vite | Frontend development environment and build tool |
| JavaScript | Frontend programming language |
| Tailwind CSS | Responsive styling |
| Lucide React | Icons |
| Recharts | Health graphs and data visualization |

### Backend

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | Backend framework and REST APIs |
| WebSockets | Real-time communication |

### Database and Authentication

| Technology | Purpose |
|---|---|
| PostgreSQL | Relational database |
| Supabase | Managed PostgreSQL database platform |
| Supabase Auth | User authentication and session management |

### Artificial Intelligence

| Technology | Purpose |
|---|---|
| Google Gemini API | AI-powered explanations and general health suggestions |

### Development and Deployment

| Technology | Purpose |
|---|---|
| Git | Version control |
| GitHub | Source code management and team collaboration |
| VS Code | Development environment |
| Vercel | Frontend deployment |
| Cloud Hosting | FastAPI backend deployment |

---

## 🏗️ System Architecture

AstroHealth will follow a frontend-backend architecture.

### Main Components

**1. Frontend — React.js**

Provides the astronaut's personal dashboard, health visualizations, alerts, and AI assistant interface.

**2. Backend — FastAPI**

Handles:

- API requests.
- Authentication verification.
- Health data processing.
- Simulated reading generation.
- Alert generation.
- Database communication.
- AI API integration.
- WebSocket communication.

**3. Database — Supabase PostgreSQL**

Stores:

- Astronaut profiles.
- Health readings.
- Historical health information.
- Generated alerts.

**4. Authentication — Supabase Auth**

Manages user authentication and secure sessions.

**5. AI Service — Gemini API**

Processes permitted, non-identifying demo health information and generates explanations and general guidance.

### Data Flow

1. The astronaut logs into the application.
2. The frontend communicates with the FastAPI backend.
3. The backend verifies the user's authentication and permissions.
4. Simulated health readings are generated.
5. The backend processes and stores the readings in PostgreSQL.
6. FastAPI WebSockets send updates to the connected frontend.
7. The frontend displays updated health information.
8. The backend evaluates readings and generates alerts.
9. The AI assistant provides explanations and general suggestions when requested.

---

## 📁 Project Structure

The project will follow a monorepo structure.

```text
AstroHealth/
│
├── backend/
│
├── frontend/
│
├── supabase/
│
├── docs/
│
├── README.md
│
├── .gitignore
│
├── .env
│
└── .env.example
```

### Folder Responsibilities

| Folder | Description |
|---|---|
| `backend/` | FastAPI backend, APIs, WebSockets, and server-side logic |
| `frontend/` | React application and user interface |
| `supabase/` | PostgreSQL database schema and SQL migrations |
| `docs/` | Project documentation and technical resources |

The internal folders and files will be organized as development progresses.

---

## 📊 Data Management

AstroHealth will initially use **simulated health data** rather than actual live astronaut sensor data.

### Simulated Health Data

The system will generate demonstration readings for:

- Heart rate.
- SpO₂.
- Body temperature.
- Activity.
- Sleep.
- Mood and well-being.

The readings will be generated at regular intervals to demonstrate real-time monitoring.

### Data Storage

Health readings will be stored in Supabase PostgreSQL with relevant information such as:

- Astronaut ID.
- Timestamp.
- Health indicator values.
- Data source.

### Data Transparency

All generated readings will be clearly identified as simulated.

The prototype will not claim that synthetic readings represent actual astronaut medical measurements.

---

## 🔄 Application Workflow

The initial application workflow will be:

```text
Astronaut Login
      |
      v
Personal Dashboard
      |
      v
Simulated Health Readings
      |
      v
FastAPI Backend
      |
      v
Data Processing
      |
      +------------------+
      |                  |
      v                  v
PostgreSQL          Alert Generation
      |                  |
      +--------+---------+
               |
               v
       FastAPI WebSockets
               |
               v
       Dashboard Updates
               |
               v
        AI Health Assistant
```

---

## 🔐 Security and Privacy

Security and privacy are important considerations in AstroHealth.

The following practices will be considered:

- Authentication through Supabase Auth.
- Protected backend API endpoints.
- User-specific access to health records.
- Secure handling of environment variables.
- API keys will remain on the backend.
- Sensitive credentials will not be committed to GitHub.
- AI requests will use synthetic or non-identifying demonstration data.
- Access permissions will be enforced by the backend and database policies where applicable.

---

## ⚠️ Project Limitations

AstroHealth is an educational prototype and demonstration system.

It has the following limitations:

1. Health readings are simulated and are not collected from actual astronauts.
2. The prototype does not connect to real wearable devices or medical sensors.
3. AI-generated suggestions are general information and not medical diagnoses.
4. Alert thresholds are illustrative prototype rules, not certified medical thresholds.
5. The system is not a certified medical device.
6. The application does not replace medical professionals or mission medical teams.
7. The system does not provide verified real-time NASA astronaut telemetry.

---

## 🚀 Future Goals

The following features may be considered for future development:

### 1. Admin / Centralized Mission Control Dashboard

A centralized dashboard for authorized mission control personnel to:

- View multiple astronauts.
- Monitor their health statuses.
- Review health alerts.
- Compare health trends.
- Access authorized astronaut health records.

### 2. Wearable Sensor Integration

Integration with actual wearable devices or sensor systems to collect health readings instead of relying only on simulated data.

### 3. Advanced Health Analysis

Explore more advanced data analysis and machine learning approaches to identify unusual health patterns.

### 4. NASA Research Data Integration

Integrate relevant publicly available NASA research datasets to provide additional scientific context and research insights.

### 5. Enhanced Monitoring

Explore additional indicators and monitoring capabilities related to astronaut health and spaceflight conditions.

---

## ⚙️ Installation and Setup

The application is currently under development. Detailed installation and configuration instructions will be added as the backend and frontend components are implemented.

The planned development environment includes:

- Python and FastAPI for the backend.
- Node.js and React.js for the frontend.
- Supabase for PostgreSQL and authentication.
- Google Gemini API for AI integration.

Environment variables and API credentials will be configured locally and must not be committed to the public repository.

---

## 👥 Team and Contributions

AstroHealth is being developed as a collaborative project for the NASA Space Apps Challenge 2026.

Team members will contribute to different areas of the application, including:

- Frontend development.
- Backend development.
- Database design.
- AI integration.
- Testing and documentation.

Contributions and improvements will be managed through Git and GitHub.

---

## 📜 Disclaimer

AstroHealth is an educational and experimental software prototype developed to demonstrate astronaut health monitoring concepts.

It is not an official NASA product, is not affiliated with or endorsed by NASA, and is not intended for actual medical decision-making.

All health readings generated by the initial prototype are simulated.

---

**Built for exploring technology-driven solutions to astronaut health monitoring.** 🚀