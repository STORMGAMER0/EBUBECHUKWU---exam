from fastapi.testclient import TestClient

from main import app
from database import Event


client =TestClient(app)

def test_add_event():
    event_data = {
        "title": "how to be a hero",
        "location": "Lagos",
        "date": "2025-08-01"
    }

    response = client.post("/events", json=event_data)

    assert response.status_code == 201
    data = response.json()

    assert data["title"] == event_data["title"]
    assert data["location"] == event_data["location"]
    assert data["date"] == event_data["date"]
    assert data["is_open"] is True
    assert "event_id" in data

def test_get_events():
    Event.clear()
    response = client.get("/events")
    assert response.status_code == 200
    assert isinstance(response.json(),dict)




def test_get_event_by_id():
    Event.clear()
    event_data = {
        "title": "how to be a hero",
        "location": "Lagos",
        "date": "2025-08-01"
    }
    post_response = client.post("/events", json = event_data)
    assert post_response.status_code == 201
    post_data = post_response.json()
    assert post_data["title"] == event_data["title"]
    assert post_data["location"] == event_data["location"]
    assert post_data["date"] == event_data["date"]
    assert post_data["is_open"] is True
    event_id = post_data["event_id"]

    get_response = client.get(f"/events/id/{event_id}")
    assert get_response.status_code == 200
    data = get_response.json()

    assert data["title"] == post_data["title"]
    assert data["location"] == post_data["location"]
    assert data["date"] == post_data["date"]
    assert data["is_open"] == True

def test_get_event_by_id_not_found():
    Event.clear()
    unfound_id = 24

    response = client.get(f"events/id/{unfound_id}")
    get_response_data = response.json()
    assert response.status_code == 404
    assert get_response_data["detail"] == "event not found"

def test_get_event_by_title():
    Event.clear()
    event_data = {
        "title": "how to be a hero",
        "location": "Lagos",
        "date": "2025-08-01"
    }
    post_response = client.post("/events", json=event_data)
    assert post_response.status_code == 201
    post_data = post_response.json()
    assert post_data["title"] == event_data["title"]
    assert post_data["location"] == event_data["location"]
    assert post_data["date"] == event_data["date"]
    assert post_data["is_open"] is True

    title = post_data["title"]

    get_response = client.get(f"/events/title/{title}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["title"] == post_data["title"]
    assert data["location"] == post_data["location"]
    assert data["date"] == post_data["date"]
    assert data["is_open"] == True
    assert "event_id" in data


def test_get_event_by_title_not_found():
    Event.clear()
    unfound_title = "bread"

    response = client.get(f"events/title/{unfound_title}")
    get_response_data = response.json()
    assert response.status_code == 404
    assert get_response_data["detail"] == "event not found"

def test_update_event():
    Event.clear()
    event_data = {
        "title": "how to be a hero",
        "location": "Lagos",
        "date": "2025-08-01"
    }
    post_response = client.post("/events", json=event_data)
    assert post_response.status_code == 201
    event_id= post_response.json()["event_id"]

    updated_data = {
        "title":"how to be a villain",
        "location" : "abuja",
    }

    put_response = client.put(f"/events/update/{event_id}", json=updated_data)
    assert put_response.status_code == 200
    updated_event = put_response.json()

    assert updated_event["title"] == "how to be a villain"
    assert updated_event["location"] == "abuja"
    assert updated_event["date"] == "2025-08-01"
    assert updated_event["is_open"] == True


def test_update_event_not_found():
    Event.clear()
    unfound_id = 24
    updated_data = {
        "title": "how to be a villain",
        "location": "abuja",
    }
    response = client.put(f"/events/update/{unfound_id}", json=updated_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "event not found"

def test_delete_event():
    Event.clear()
    event_data = {
        "title": "how to be a hero",
        "location": "Lagos",
        "date": "2025-08-01"
    }
    post_response = client.post("/events", json=event_data)
    assert post_response.status_code == 201
    event_id = post_response.json()["event_id"]

    delete_response= client.delete(f"/events/delete/{event_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["detail"] == "event deleted successfully"


def test_delete_event_not_found():
    Event.clear()
    unfound_id = 24
    response = client.delete(f"/events/delete/{unfound_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"

def test_close_event():
    Event.clear()
    event_data = {
        "title": "how to be a hero",
        "location": "Lagos",
        "date": "2025-08-01"
    }
    post_response = client.post("/events", json=event_data)
    assert post_response.status_code == 201
    event_id = post_response.json()["event_id"]


    close_response = client.put(f"/events/close/{event_id}")
    assert close_response.status_code == 200
    closed_event = close_response.json()

    assert closed_event["detail"] == "event closed successfully"


def test_close_already_closed_event():
    Event.clear()

    event_data = {
        "title": "already closed",
        "location": "Abuja",
        "date": "2025-11-11"
    }
    post_response = client.post("/events", json=event_data)
    event_id = post_response.json()["event_id"]

    client.put(f"/events/close/{event_id}")

    second_response = client.put(f"/events/close/{event_id}")
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "event is already closed"

def test_close_event_not_found():
    Event.clear()
    unfound_id = 24

    response = client.put(f"/events/close/{unfound_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "event not found"


def test_open_event():
    Event.clear()
    event_data = {
        "title": "how to be a hero",
        "location": "Lagos",
        "date": "2025-08-01"
    }
    post_response = client.post("/events", json=event_data)
    assert post_response.status_code == 201
    event_id = post_response.json()["event_id"]

    close_response = client.put(f"/events/close/{event_id}")
    assert close_response.status_code == 200

    assert close_response.json()["detail"] == "event closed successfully"

    open_response = client.put(f"/events/open/{event_id}")
    assert open_response.status_code == 200
    opened_event = open_response.json()

    assert opened_event["detail"] == "event opened successfully"

def test_open_event_not_found():
    Event.clear()
    unfound_id = 24

    response = client.put(f"/events/open/{unfound_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "event not found"
