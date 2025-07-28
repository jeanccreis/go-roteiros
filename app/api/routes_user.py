from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.db.models import User
from app.db.database import get_db
from app.services.auth_service import get_current_active_user, get_user_by_email, verify_password, hash_password
from app.auth.auth_handler import decode_token
from app.schemas.user import UserUpdate, UserResponse, PasswordChange
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> User:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")

    email = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = await get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return user

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await get_current_active_user(current_user)

@router.put("/me", response_model=UserResponse)
async def update_user_profile(
    update_data: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    current_user.full_name = update_data.full_name
    current_user.email = update_data.email

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)

    return current_user

@router.put("/me/password")
async def update_password(
    new_password: PasswordChange,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    if not verify_password(new_password.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Senha atual incorreta")

    current_user.hashed_password = hash_password(new_password.new_password)

    db.add(current_user)
    await db.commit()
    return {"detail": "Senha atualizada com sucesso"}


@router.delete("/me")
async def delete_user_account(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    await db.delete(current_user)
    await db.commit()
    
    return JSONResponse(
        status_code=200,
        content={"detail": "Usuário deletado com sucesso. Faça logout"}
    )