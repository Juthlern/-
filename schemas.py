from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from models import User

# Address Schemas 

class AddressBase(BaseModel):
    street: str
    city: str
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: str
    is_primary: Optional[bool] = False

class AddressCreate(AddressBase):
    user_id: UUID

class AddressUpdate(AddressBase):
    pass

class Address(AddressBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Order Schemas 

class OrderBase(BaseModel):
    product_name: str
    product_description: Optional[str] = None
    product_price: float
    quantity: int = 1
    total_amount: float
    status: Optional[str] = "pending"

class OrderCreate(OrderBase):
    user_id: UUID
    address_id: UUID

class OrderUpdate(OrderBase):
    pass

class Order(OrderBase):
    id: UUID
    user_id: UUID
    address_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# User Schemas 

class UserBase(BaseModel):
    username: str
    email: EmailStr
    description: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    description: Optional[str] = None

class User(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    addresses: List[Address] = []
    orders: List[Order] = []

    model_config = ConfigDict(from_attributes=True)

class UserListResponse(BaseModel):
    total: int
    users: List[User]