"""
Multi-Agent Learning System
===========================

An intelligent multi-agent system for personalized learning, featuring:
- Academic planning with task and schedule management
- Spaced repetition using the SM-2 algorithm
- Topic dependency tracking and learning path optimization
- AI-powered prerequisite discovery via web search

Powered by Google's Gemini 2.0 and the Agent Development Kit (ADK).

Usage:
    python main.py

Author: Shreyas B S
License: MIT
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import asyncio
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from manager_agent.agent import manager_agent
from utils import call_agent_async, display_state

load_dotenv()

# Configuration
APP_NAME = "SagePath"
USER_ID = os.getenv("USER_ID", "user")  # Configurable via environment
DB_PATH = os.getenv("DB_PATH", "./learning_mas.db")

# Initialize SQLite-based persistent session service
db_url = f"sqlite:///{DB_PATH}"
session_service = DatabaseSessionService(db_url=db_url)

# Default state structure for new sessions
initial_state = {
    "user_name": USER_ID.title(),
    "known_topics": [],
    "learning_tasks": [],
    "review_schedule": [],
    "interaction_history": [],
    "study_progress": [],
    "prereq_map": {},
}

async def main_async():
    # Check existing sessions
    existing_sessions = session_service.list_sessions(app_name=APP_NAME, user_id=USER_ID)
    if existing_sessions.sessions:
        session = existing_sessions.sessions[0]
        print(f"Continuing session: {session.id}")
    else:
        session = session_service.create_session(
            app_name=APP_NAME, 
            user_id=USER_ID, 
            state=initial_state
        )
        print(f"New session created: {session.id}")

    SESSION_ID = session.id

    runner = Runner(
        agent=manager_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    print(f"\nWelcome to your Personalized Learning Agent {USER_ID.title()}!")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break


        # Route the query to the agent
        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)

        # Show updated session state
        display_state(session_service, APP_NAME, USER_ID, SESSION_ID)

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()