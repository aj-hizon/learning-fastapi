from fastapi import Depends, HTTPException, status
from src.utils.jwt import verify_access_token
from src.services.auth_service import AuthService
from src.routers.auth import oauth2_scheme

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        service: AuthService = Depends()
):
    payload = verify_access_token(token)
    if not payload: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user = await service.collection.find_one({"username": username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user