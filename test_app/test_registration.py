from fastapi.testclient import TestClient

from main import app
from database import Event, Registrations, User


client =TestClient(app)

def test_register_user():
    Event.clear()
    User.clear()
    Registrations.clear()

    user_data = {
        "user_id": 1,
        "name": "Test User",
        "is_active": True
    }
    User[1] = user_data

    event_data = {
        "event_id": 1,
        "title": "Test Event",
        "location": "Test Location",
        "date": "2025-08-01",
        "is_open": True
    }
    Event[1] = event_data

    registration_data = {
        "user_id": 1,
        "event_id": 1,
        "registration_date": "2025-01-01T00:00:00"
    }

    response = client.post("/registrations/", json=registration_data)

    assert response.status_code == 201
    data = response.json()

    assert data["user_id"] == registration_data["user_id"]
    assert data["event_id"] == registration_data["event_id"]
    assert data["registration_date"] == registration_data["registration_date"]
    assert data["attended"] is False
    assert "registration_id" in data

def test_get_registrations():
    Registrations.clear()
    
    
    registration_data = {
        "registration_id": 1,
        "user_id": 1,
        "event_id": 1,
        "registration_date": "2025-01-01T00:00:00",
        "attended": False
    }
    Registrations[1] = registration_data

    response = client.get("/registrations")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, dict)
    assert len(data) == 1
    assert data["1"] == registration_data

def test_mark_attendance():
    Registrations.clear()
    
    registration_data = {
        "registration_id": 1,
        "user_id": 1,
        "event_id": 1,
        "registration_date": "2025-01-01T00:00:00",
        "attended": False
    }
    Registrations[1] = registration_data

    response = client.put("/registrations/1/attend")

    assert response.status_code == 200
    data = response.json()

    assert data["detail"] == "user1 marked present!"
    assert Registrations[1]["attended"] is True

def test_mark_attendance_not_found():
    Registrations.clear()
    
    response = client.put("/registrations/999/attend")

    assert response.status_code == 404
    data = response.json()

    assert data["detail"] == "event not found"

def test_get_user_registrations():
    Registrations.clear()
    User.clear()

    user_data = {
        "user_id": 1,
        "name": "Test User",
        "is_active": True
    }
    User[1] = user_data

    registration_data = {
        "registration_id": 1,
        "user_id": 1,
        "event_id": 1,
        "registration_date": "2025-01-01T00:00:00",
        "attended": False
    }
    Registrations[1] = registration_data

    response = client.get("/registrations/user/1")

    assert response.status_code == 200
    data = response.json()

    assert data["user_id"] == 1
    assert len(data["registrations"]) == 1
    assert data["registrations"][0] == registration_data

def test_get_user_registrations_not_found():
    Registrations.clear()
    User.clear()

    response = client.get("/registrations/user/999")

    assert response.status_code == 404
    data = response.json()

    assert data["detail"] == "User not found"

    

