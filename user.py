
from db import Base
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean
from typing import Optional

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    role = Column(String, default="user") 
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String)


# --- Data Models (Pydantic) ---
class User(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool = True
    role: str = "user"  # Default role is 'user'
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    full_name: Optional[str] = None
    role: str = "user"  # Default role is 'user'
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
	
