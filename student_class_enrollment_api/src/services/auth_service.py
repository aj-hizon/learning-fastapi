from fastapi import Depends, HTTPException, status
from src.db.mongodb import get_users_collection
from src.models.user import UserSignup, UserInDB, User, UserLogin
from src.utils.security import hash_password, verify_password
from src.utils.jwt import create_access_token

class AuthService:
    def __init__(self, collection=Depends(get_users_collection)):
        self.collection = collection

    async def signup(self, user:UserSignup):
        existing_user = await self.collection.find_one({"username": user.username})
        if existing_user: 
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        hashed_password = hash_password(user.password)
        user_dict = user.model_dump()
        user_dict["hashed_password"] = hashed_password
        del user_dict["password"]
        result = await self.collection.insert_one(user_dict)
        user_dict["id"] = str(result.inserted_id)
        user_dict.pop("_id", None)
        return user_dict
    
    async def authenticate_user(self, username: str, password: str) -> UserInDB:
        user = await self.collection.find_one({"username": username})
        if not user or not verify_password(password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return UserInDB(**user)
    
    def create_access_token(self, username: str) -> str:
        return create_access_token({"sub": username})

        
