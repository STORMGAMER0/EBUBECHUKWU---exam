from fastapi.testclient import TestClient

from main import app
from database import Registrations, User
from routes.user import list_users_who_attended


client =TestClient(app)

def test_create_user():
    payload = {
        "name" : "kami",
        "email" : "eobi816@gmail.com"
    }

    post_response = client.post("/users", json=payload)
    assert post_response.status_code == 201
    data = post_response.json()

    assert data["name"] == "kami"
    assert data["email"] == "eobi816@gmail.com"
    assert data["is_active"] is True
    assert "user_id" in data

def test_get_users():
    User.clear()
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_get_user_by_id():
    User.clear()
    payload = {
        "name": "kami",
        "email": "eobi816@gmail.com"
    }

    post_response = client.post("/users", json=payload)
    assert post_response.status_code == 201
    user_id = post_response.json()["user_id"]

    get_response = client.get(f"/users/id/{user_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert data["is_active"] == True

def test_get_user_by_id_not_found():
    User.clear()
    unfound_id = 60
    response = client.get(f"/users/id/{unfound_id}")
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "user not found"

def test_get_user_name():
    User.clear()
    payload = {
        "name": "kami",
        "email": "eobi816@gmail.com"
    }

    post_response = client.post("/users", json=payload)
    assert post_response.status_code == 201
    name = post_response.json()["name"]

    get_response = client.get(f"/users/name/{name}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert data["is_active"] == True
    assert "user_id" in data

def test_get_user_name_not_found():
    User.clear()
    unfound_name = "nonexistent"
    response = client.get(f"/users/name/{unfound_name}")
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "User not found"

def test_update_user():
    User.clear()
    payload = {
        "name": "kami",
        "email": "eobi816@gmail.com"
    }
    post_response = client.post("/users", json=payload)
    assert post_response.status_code == 201
    user_id = post_response.json()["user_id"]
    update_payload = {
        "name": "updated_kami",
    }
    update_response = client.put(f"/users/update/{user_id}", json=update_payload)
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == update_payload["name"]
    assert data["email"] == payload["email"]
    assert data["is_active"] == True

def test_update_user_not_found():
    User.clear()
    unfound_id = 60
    update_payload = {
        "name": "updated_kami",
    }
    response = client.put(f"/users/update/{unfound_id}", json=update_payload)
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "user not found"
    
def test_delete_user():
    User.clear()
    payload = {
        "name": "kami",
        "email": "eobi917@gmail.com"
    }
    post_response = client.post("/users", json=payload)
    assert post_response.status_code == 201
    user_id = post_response.json()["user_id"]

    delete_response = client.delete(f"/users/delete/{user_id}")
    assert delete_response.status_code == 200
    data = delete_response.json()
    assert data["detail"] == "user deleted successfully"

def test_delete_user_not_found():
    User.clear()
    unfound_id = 60
    response = client.delete(f"/users/delete/{unfound_id}")
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "User not found"

def test_deactivate_user():
    User.clear()
    payload = {
        "name": "kami",
        "email": "eobi917@gmail.com"
    }
    post_response = client.post("/users", json=payload)
    assert post_response.status_code == 201
    user_id = post_response.json()["user_id"]

    deactivate_response = client.put(f"/users/deactivate/{user_id}")
    assert deactivate_response.status_code == 200
    data = deactivate_response.json()
    assert data["detail"] == f"user {user_id} deactivated successfully"

def test_deactivate_user_not_found():
    User.clear()
    unfound_id = 60
    response = client.put(f"/users/deactivate/{unfound_id}")
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "user not found"

def test_activate_user():
    User.clear()
    payload = {
        "name": "kami",
        "email": "eobi917@gmail.com"
    }
    post_response = client.post("/users", json=payload)
    assert post_response.status_code == 201
    user_id = post_response.json()["user_id"]

    deactivate_response = client.put(f"/users/deactivate/{user_id}")
    assert deactivate_response.status_code == 200
    data = deactivate_response.json()
    assert data["detail"] == f"user {user_id} deactivated successfully"


    activate_response = client.put(f"/users/activate/{user_id}")
    assert activate_response.status_code == 200
    data = activate_response.json()
    assert data["detail"] == f"user {user_id} activated successfully"

def test_activate_user_not_found():
    User.clear()
    unfound_id = 60
    response = client.put(f"/users/activate/{unfound_id}")
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "user not found"


def test_list_users_who_attended():
    Registrations.clear()
    
    Registrations[1] = {
        "user_id": 1,
        "event_id": 1,
        "attended": True
    }
    Registrations[2] = {
        "user_id": 2,
        "event_id": 1,
        "attended": False
    }
    Registrations[3] = {
        "user_id": 3,
        "event_id": 2,
        "attended": True
    }

   
    result = list_users_who_attended()

    
    expected = {"user1", "user3"}


    assert isinstance(result, set)
    assert result == expected



    
