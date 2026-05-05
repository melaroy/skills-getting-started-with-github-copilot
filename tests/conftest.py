"""
Pytest configuration and fixtures for FastAPI tests.
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Provide a TestClient for the FastAPI app with a clean database state.
    Resets activities to initial state before each test.
    """
    # Reset activities to initial state before each test
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Develop basketball skills and compete in tournaments",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn and play tennis with fellow students",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 10,
            "participants": ["sarah@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform in plays and develop acting skills",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["lucas@mergington.edu", "mia@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and sculpture techniques",
            "schedule": "Fridays, 2:00 PM - 4:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific concepts",
            "schedule": "Mondays, 3:30 PM - 4:30 PM",
            "max_participants": 16,
            "participants": ["noah@mergington.edu", "ava@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and argumentation skills",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["ethan@mergington.edu"]
        }
    })
    
    return TestClient(app)
