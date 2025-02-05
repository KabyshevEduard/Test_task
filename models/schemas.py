from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

class UserRegisterSchema(BaseModel):
    email: EmailStr = Field(..., description='Email')
    password: str = Field(..., min_length=8, max_length=100, description='password 8-100')
    password_check: str = Field(..., min_length=8, max_length=100, description='password 8-100')
    full_name: str = Field(..., min_length=5, max_length=50, description='full_name')


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(..., description='Email')
    password: str = Field(..., min_length=8, max_length=100, description='password 8-100')


class AccountsResponse(BaseModel):
    id: int
    balance: float


class TransactionSchema(BaseModel):
    unq_id: str
    amount: float

class AccountSchema(BaseModel):
    balance: float


class AllUsersResponseSchema(BaseModel):
    id: int
    email: str
    full_name: str
    is_admin: bool
    accounts: Optional[List[AccountSchema]]


class CreateUserSchema(BaseModel):
    email: EmailStr = Field(..., description='Email')
    password: str = Field(..., min_length=8, max_length=100, description='password 8-100')
    full_name: str = Field(..., min_length=5, max_length=50, description='full_name')
    is_admin: bool

class UserUpdateSchema(BaseModel):
    email: Optional[EmailStr] = Field(..., description='Email')
    full_name: Optional[str] = Field(..., max_length=50, description='Full name')
    is_admin: Optional[bool]
    password: Optional[str] = Field(..., min_length=8, max_length=100, description='password 8-100')


class WebHookSchema(BaseModel):
    transaction_id: str
    account_id: int
    user_id: int
    amount: float
    signature: str