# 🎯 Synergy AI - Multi-Agent Productivity Platform

**Synergy AI** is a production-grade Agentic Application built with **Google Gemini (ADK)**, **FastAPI**, and **Streamlit**. It orchestrates specialized AI agents to help users manage daily goals, prepare for interviews, and search for jobs efficiently.

![Dashboard Screenshot](assets/dashboard_view.png)

## 🚀 Key Features

*   **🧠 Multi-Agent Orchestration:** Uses Sequential and Parallel agent workflows (Study, Wellness, Job Search).
*   **🎤 AI Mock Interviewer:** An interactive, state-based agent that conducts technical interviews and provides graded feedback.
*   **🔍 Live Job Search:** Integrates with Google Search tools to find real-time job listings.
*   **🐳 Microservices Architecture:** Fully containerized Frontend and Backend using Docker Compose.

## 🛠️ Tech Stack

*   **LLM:** Google Gemini 2.5 Flash (via Google ADK)
*   **Backend:** FastAPI, Python 3.11, AsyncIO
*   **Frontend:** Streamlit
*   **DevOps:** Docker, Docker Compose
*   **Database:** SQLite (Async)

## 📦 Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/synergy-ai-platform.git
    cd synergy-ai-platform
    ```

2.  **Setup Environment Variables**
    Create a `.env` file in `backend/` with your API key:
    ```env
    GOOGLE_API_KEY=your_actual_key_here
    DATABASE_URL=sqlite+aiosqlite:///../data/synergy_ai.db
    ```

3.  **Run with Docker** (Recommended)
    ```bash
    docker compose up --build
    ```

4.  **Access the App**
    *   Frontend: http://localhost:8501
    *   Backend API Docs: http://localhost:8000/docs

## 🏗️ Architecture

```mermaid
graph LR
    User[User UI] <--> Streamlit
    Streamlit <--> FastAPI
    FastAPI <--> Runner[ADK Runner]
    Runner <--> Agents[Gemini Agents]
    Agents <--> Tools[Google Search / Wellness DB]