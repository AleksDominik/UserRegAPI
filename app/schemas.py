from lib2to3.pgen2.token import OP
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime 

# Shared properties
class UserBase(BaseModel):
    # id :Optional[int]=None
    email: Optional[EmailStr] = None
    # is_superuser: bool = False

# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    # password: Optional[str] = None
    
# Properties to receive via API on creation
class EmailCheck(BaseModel):
    email: EmailStr


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None
    


class UserInDBBase(UserBase):

    id: Optional[int] = None
    time_created :Optional[datetime]=None
    time_updated :Optional[datetime]=None
    is_active: Optional[bool] = False

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    password: str
    pass

class Token(User):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None


class Msg(BaseModel):
    msg: str
