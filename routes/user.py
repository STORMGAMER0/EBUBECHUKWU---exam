from typing import Dict

from fastapi import APIRouter, status

from database import Speaker, User
from schemas.user import CreateUser, ResponseUser, UpdateUser
from services.user import UserService
from services.registration import RegistrationService


user_router = APIRouter()


@user_router.post("/users", status_code=status.HTTP_201_CREATED, response_model=ResponseUser)
def create_user(user:CreateUser):
    new_user = UserService.create_user(user)
    return new_user

@user_router.get("/users", status_code=status.HTTP_200_OK,response_model=Dict[int, ResponseUser])
def get_users():
    return User

@user_router.get("/users/id/{user_id}", status_code=status.HTTP_200_OK,response_model=ResponseUser)
def get_user_by_id(user_id : int):
    user = UserService.get_user(user_id)
    return user

@user_router.get("/users/name/{name}", status_code=status.HTTP_200_OK,response_model=ResponseUser)
def get_user_by_name(name:str):
    name = UserService.get_user_name(name)
    return name

@user_router.put("/users/update/{user_id}", status_code=status.HTTP_200_OK,response_model=ResponseUser)
def update_user(user_id : int, update: UpdateUser):
    update = UserService.update_user(user_id,update)
    return update

@user_router.delete("/users/delete/{user_id}",status_code=status.HTTP_200_OK)
def delete_user(user_id:int):
    UserService.delete_user(user_id)
    return {"detail":"user deleted successfully"}

@user_router.put("/users/deactivate/{user_id}", status_code=status.HTTP_200_OK)
def deactivate_user(user_id:int):
    UserService.deactivate_user(user_id)
    return {"detail":f"user {User[user_id]["user_id"]} deactivated successfully"}

@user_router.put("/users/activate/{user_id}", status_code=status.HTTP_200_OK)
def activate_user(user_id:int):
    UserService.activate_user(user_id)
    return {"detail": f"user {User[user_id]["user_id"]} activated successfully"}

@user_router.get("/users/attended")
def list_users_who_attended():
    return RegistrationService.list_users_who_attended()


