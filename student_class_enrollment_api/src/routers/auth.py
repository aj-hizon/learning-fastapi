from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from src.models.user import UserSignup
from src.services.auth_service import AuthService

auth_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")

@auth_router.post("/signup", response_model=dict)
async def signup(user: UserSignup, service: AuthService = Depends()):
    user_data = await service.signup(user)
    return {"message": "User created successfully", "user": user_data}  

@auth_router.post("/signin", response_model=dict)
async def signin(form_data: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends()):
    user = await service.authenticate_user(form_data.username, form_data.password)
    access_token = service.create_access_token(user.username)
    return {"access_token": access_token, "token_type": "bearer"}