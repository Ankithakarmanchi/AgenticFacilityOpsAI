# 🏢 Agentic AI Facility Operations Platform

An enterprise-grade AI-powered Facility Operations Platform designed to monitor, analyze, and optimize building operations using multiple intelligent AI agents.

The platform is being developed with a scalable micro-agent architecture where each AI agent independently analyzes a specific facility management domain while collaborating through a common backend infrastructure.

---

# 📌 Project Overview

Modern commercial buildings generate enormous amounts of operational data, including energy consumption, equipment health, occupancy, and security events.

Managing this data manually is difficult and often results in:

- High energy consumption
- Delayed maintenance
- Increased operational costs
- Poor resource utilization

This project uses AI-powered agents to automate facility monitoring, provide actionable insights, and support intelligent decision-making.

---

# 🚀 Current Features

## ✅ Authentication

- Login Interface
- Dashboard Layout

## ✅ Energy Agent

- Reads real ASHRAE Energy Dataset
- Real-time KPI generation
- Building statistics
- Average meter reading
- Peak meter reading
- Energy savings analysis
- Cost savings estimation
- Interactive dashboard

## ✅ Backend API

- FastAPI REST APIs
- Modular Agent Architecture
- Automatic Agent Registration
- Reusable Base Agent Service

## ✅ Frontend

- Component-based UI
- Responsive Dashboard
- Chart.js Integration
- Dynamic API Integration

---

# 🏗️ Project Architecture

```
                +-----------------------+
                |      Frontend         |
                | HTML • CSS • JS       |
                +----------+------------+
                           |
                           |
                     REST API Calls
                           |
                           ▼
                +-----------------------+
                |      FastAPI          |
                |   Backend Services    |
                +----------+------------+
                           |
          ---------------------------------------
          |            |            |            |
          ▼            ▼            ▼            ▼
   Energy Agent  Maintenance  Occupancy   Security
                     Agent        Agent      Agent
                           |
                           ▼
                  AI Analytics Engine
                           |
                           ▼
                   Facility Intelligence
```

---

# ⚙️ Technology Stack

## Frontend

- HTML5
- CSS3
- JavaScript
- Chart.js

## Backend

- FastAPI
- Python

## Data Processing

- Pandas
- NumPy

## Dataset

- ASHRAE Great Energy Predictor III Dataset

## Version Control

- Git
- GitHub

---

# 📂 Project Structure

```
AgenticFacilityOpsAI
│
├── backend/
│   ├── api/
│   ├── core/
│   ├── services/
│   ├── data/
│   ├── app.py
│   └── requirements.txt
│
├── components/
│
├── css/
│
├── js/
│
├── pages/
│
├── images/
│
├── assets/
│
├── data/
│
├── index.html
│
└── README.md
```

---

# 📊 Current Dashboard

The dashboard currently provides:

- Total Buildings
- Total Records
- Average Meter Reading
- Peak Meter Reading
- Energy Savings
- Cost Savings
- AI Agent Status

All analytics displayed are generated from the integrated dataset.

---

# 🔄 Development Roadmap

## ✅ Phase 1

- Login Page
- Dashboard
- Energy Agent
- FastAPI Backend
- Dataset Integration

## 🚧 Phase 2

- Maintenance Agent
- Occupancy Agent
- Security Agent
- Cost Optimization Agent

## 🚧 Phase 3

- AI Forecasting
- Predictive Maintenance
- Occupancy Prediction
- Energy Optimization
- Cross-Agent Decision Making

## 🚧 Phase 4

- Report Generation
- Alerts & Notifications
- AI Recommendations
- Facility Intelligence Engine

---

# ▶️ Installation

## Clone Repository

```bash
git clone https://github.com/Ankithakarmanchi/AgenticFacilityOpsAI.git
```

## Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app:app --reload
```

Backend:

```
http://127.0.0.1:8000
```

## Frontend

Open

```
pages/dashboard.html
```

using Live Server.

---

# 📈 Future Enhancements

- Predictive Maintenance
- Energy Forecasting
- AI Recommendation Engine
- Real-time Alerts
- Facility Intelligence Dashboard
- Multi-Agent Collaboration
- Cloud Deployment
- User Authentication & Role Management

---

# 👩‍💻 Developer

**Ankitha Karmanchi**

Computer Science Engineering Student

Passionate about AI, Machine Learning, Full Stack Development, and Intelligent Software Systems.

---

# ⭐ Repository

If you found this project useful, consider giving it a ⭐ on GitHub.