from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'

class TokenPayload(BaseModel):
    sub: Optional[int] = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class AccountBase(BaseModel):
    name: str
    platform: Optional[str] = None
    type: Optional[str] = None
    manual_balance: Optional[float] = 0.0
    manual_override: Optional[bool] = True
    currency: Optional[str] = 'USD'
    update_mode: Optional[str] = 'manual'
    notes: Optional[str] = None

class AccountCreate(AccountBase):
    pass

class AccountOut(AccountBase):
    id: int
    user_id: int
    last_updated: Optional[datetime] = None
    class Config:
        orm_mode = True

class TransactionBase(BaseModel):
    account_id: int
    tx_type: str
    amount: float
    currency: Optional[str] = 'USD'
    description: Optional[str] = None
    ts: int

class TransactionCreate(TransactionBase):
    pass

class TransactionOut(TransactionBase):
    id: int
    user_id: int
    class Config:
        orm_mode = True
