from fastapi import HTTPException

from database import User
from schemas.user import CreateUser, UpdateUser


class UserService:
    @staticmethod
    def create_user(new_user:CreateUser):
        user_id = len(User)+1
        user_data = new_user.model_dump()
        user_data["user_id"] = user_id
        user_data["is_active"] = True
        User[user_id] = user_data
        return user_data

    @staticmethod
    def get_user(user_id:int):
        if user_id not in User:
            raise HTTPException(status_code=404, detail="user not found")
        return User[user_id]

    @staticmethod
    def get_user_name(name : str):
        for values in User.values():
            if values["name"] == name:
                return values
        raise HTTPException(status_code=404, detail="User not found")

    @staticmethod
    def update_user(user_id: int, update_data : UpdateUser):
        if user_id not in User:
            raise HTTPException(status_code=404, detail="user not found")
        user= User[user_id]
        if update_data.name is not None:
            user["name"] = update_data.name
        if update_data.email is not None:
            user["email"] = update_data.email

        return user
    @staticmethod
    def delete_user(user_id:int):
        if user_id not in User:
            raise HTTPException(status_code=404, detail="User not found")
        del User[user_id]

    @staticmethod
    def deactivate_user(user_id:int):
        if user_id not in User:
            raise HTTPException(status_code=404, detail="user not found")
        user = User[user_id]

        if not user.get("is_active", True):
            raise HTTPException(status_code=400, detail="User is already deactivated")

        user["is_active"] = False
        return user

    @staticmethod
    def activate_user(user_id: int):
        if user_id not in User:
            raise HTTPException(status_code=404, detail="user not found")
        user = User[user_id]

        if user.get("is_active", False):
            raise HTTPException(status_code=400, detail="User is already active")

        user["is_active"] = True
        return user




