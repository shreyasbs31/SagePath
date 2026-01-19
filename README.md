# Multi-Agent Learning System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Google AI](https://img.shields.io/badge/Google_AI-Gemini_2.0-4285F4?style=for-the-badge&logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

**An intelligent multi-agent system for personalized learning, powered by Google's Gemini 2.0 and the Agent Development Kit (ADK)**

[Features](#-features) • [Architecture](#-architecture) • [Quick Start](#-quick-start) • [Usage](#-usage) • [License](#-license)

</div>

---

## 📋 Overview

This project implements a **hierarchical multi-agent system** designed to optimize personal learning through:
- **Smart Academic Planning** - Automated study schedules and task management
- **Spaced Repetition (SM-2)** - Science-backed memory retention using the SuperMemo algorithm
- **Prerequisite Dependency Tracking** - Intelligent topic ordering based on learning dependencies
- **AI-Powered Research** - Real-time web search for prerequisite discovery

## Features

| Feature | Description |
|---------|-------------|
| **Manager Agent** | Central orchestrator that routes queries to specialized sub-agents |
| **Academic Planner** | Creates weekly study plans, manages tasks with due dates |
| **Spaced Repetition Engine** | Implements SM-2 algorithm for optimal review scheduling |
| **Dependency Tracker** | Maps topic prerequisites and suggests learning paths |
| **Web Search Integration** | Auto-discovers prerequisites via Google Search |
| **Persistent Sessions** | SQLite-backed state management across sessions |
| **Progress Tracking** | Visual progress indicators with completion status |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Manager Agent                          │
│          (Query Routing & Orchestration)                    │
└──────────────┬──────────────┬──────────────┬───────────────┘
               │              │              │
    ┌──────────▼────┐  ┌──────▼──────┐  ┌───▼─────────────┐
    │   Academic    │  │   Spaced    │  │   Dependency    │
    │   Planning    │  │ Repetition  │  │     Engine      │
    │    Agent      │  │    Agent    │  │     Agent       │
    └───────────────┘  └─────────────┘  └────────┬────────┘
                                                 │
                                        ┌────────▼────────┐
                                        │  Search Agent   │
                                        │ (Google Search) │
                                        └─────────────────┘
```

### Agent Responsibilities

| Agent | Purpose | Key Tools |
|-------|---------|-----------|
| **Manager Agent** | Routes queries, maintains context | Sub-agent delegation |
| **Academic Planning** | Task scheduling, weekly plans | `add_task`, `generate_schedule`, `update_study_progress` |
| **Spaced Repetition** | Memory optimization | `record_review_result`, `get_due_reviews` (SM-2 algorithm) |
| **Dependency Engine** | Learning path optimization | `can_learn`, `auto_update_prereqs`, `suggest_next_topics` |
| **Search Agent** | Research & discovery | `google_search` |

## Quick Start

### Prerequisites

- Python 3.10+
- Google AI API Key (for Gemini access)

### Installation

```bash
# Clone the repository
git clone https://github.com/shreyasbs31/Multi-Agent-System-for-Learning.git
cd Multi-Agent-System-for-Learning

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your Google AI API key
```

### Configuration

Create a `.env` file with:
```env
GOOGLE_API_KEY=your_google_ai_api_key_here
```

### Run

```bash
python main.py
```

## Usage Examples

### Academic Planning
```
You: Add DBMS revision task for Friday
Agent: Added task: 'DBMS revision' due by 24-01-2026

You: What's my study plan this week?
Agent: Here's your weekly study plan...
```

### Spaced Repetition
```
You: What should I revise today?
Agent: Topics due for review: ['Binary Trees', 'Graph Algorithms']

You: I reviewed Binary Trees and scored 4
Agent: Review recorded. Next review in 6 days.
```

### Dependency Tracking
```
You: Can I learn Dynamic Programming?
Agent: Missing prerequisites: ['Recursion', 'Arrays']
       Complete these first!

You: I've finished learning Recursion
Agent: Marked 'Recursion' as learned.
```

### Progress Tracking
```
You: I finished 80% of Graphs
Agent: Progress updated for 'Graphs': 80%

You: I completed 100% of Recursion  
Agent: Progress updated: 100% (completed & added to known topics)
```

## State Management

The system maintains persistent state using SQLite:

```python
{
    "user_name": "User",
    "known_topics": ["Arrays", "Recursion", "OOP"],
    "learning_tasks": [{"task": "...", "due_date": "...", "created_at": "..."}],
    "review_schedule": [{"topic": "...", "next_review_due": "...", "easiness": 2.5}],
    "study_progress": [{"topic": "...", "percent": 80, "completed": false}],
    "prereq_map": {"Dynamic Programming": ["Recursion", "Arrays"]}
}
```

## SM-2 Algorithm Implementation

The spaced repetition agent uses the **SuperMemo SM-2 algorithm**:

```
EF' = EF + (0.1 - (5-q) × (0.08 + (5-q) × 0.02))

Where:
- EF = Easiness Factor (≥1.3)
- q = Quality of response (0-5 scale)
- Interval grows: 1 → 6 → 6×EF → ...
```

| Score | Meaning | Effect |
|-------|---------|--------|
| 5 | Perfect recall | Increase interval significantly |
| 4 | Minor hesitation | Increase interval |
| 3 | Difficult recall | Maintain current interval |
| 2 | Hard to remember | Reset repetitions |
| 1 | Barely recalled | Reset to 1-day interval |
| 0 | Complete blackout | Reset completely |

## Project Structure

```
Multi-Agent-System-for-Learning/
├── main.py                    # Application entry point
├── utils.py                   # Helper functions & state management
├── colours_utils.py           # Terminal output formatting
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── .gitignore                # Git ignore rules
├── README.md                 # Documentation
└── manager_agent/
    ├── __init__.py
    ├── agent.py              # Manager agent definition
    └── sub_agents/
        ├── __init__.py
        ├── academic_planning_agent/
        │   ├── __init__.py
        │   └── agent.py      # Task & schedule management
        ├── spaced_repetition_agent/
        │   ├── __init__.py
        │   └── agent.py      # SM-2 implementation
        ├── dependency_agent/
        │   ├── __init__.py
        │   └── agent.py      # Prerequisite tracking
        └── search_agent/
            ├── __init__.py
            └── agent.py      # Google Search integration
```

## Tech Stack

- **Language**: Python 3.10+
- **AI Framework**: Google Agent Development Kit (ADK)
- **LLM**: Gemini 2.0 Flash
- **Database**: SQLite with SQLAlchemy
- **Tools**: Google Search API, Async/Await patterns

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Google Agent Development Kit](https://github.com/google/adk-python) for the agent framework
- [SuperMemo SM-2 Algorithm](https://www.supermemo.com/en/archives1990-2015/english/ol/sm2) for spaced repetition

---

<div align="center">

**Built with ❤️ for better learning**

⭐ Star this repo if you find it helpful!

</div>
