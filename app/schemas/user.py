from pydantic import BaseModel, EmailStr, validator
import re

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str

    @validator("password")
    def validate_password(cls, v):
        """
        Regras de senha segura:
        - Mínimo 8 caracteres
        - Pelo menos uma letra maiúscula
        - Pelo menos uma letra minúscula
        - Pelo menos um número
        - Pelo menos um caractere especial
        """
        if len(v) < 8:
            raise ValueError("A senha deve ter pelo menos 8 caracteres")
        if not re.search(r"[A-Z]", v):
            raise ValueError("A senha deve conter pelo menos uma letra maiúscula")
        if not re.search(r"[a-z]", v):
            raise ValueError("A senha deve conter pelo menos uma letra minúscula")
        if not re.search(r"\d", v):
            raise ValueError("A senha deve conter pelo menos um número")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("A senha deve conter pelo menos um caractere especial")

        return v

    @validator("full_name")
    def validate_name(cls, v):
        if len(v.strip()) < 3:
            raise ValueError("O nome deve ter pelo menos 3 caracteres")
        return v


class UserUpdate(BaseModel):
    full_name: str
    email: EmailStr


class PasswordChange(BaseModel):
    current_password: str
    new_password: str

    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    disabled: bool

    class Config:
        from_attributes = True