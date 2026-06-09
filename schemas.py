from pydantic import BaseModel, validator
from datetime import datetime

class EventCreate(BaseModel):
    name: str
    date: datetime
    total_seats: int

class EventResponse(BaseModel):
    id: int
    name: str
    date: datetime
    total_seats: int
    available_seats: int
    created_at: datetime

    class Config:
        from_attributes = True

class RegistrationCreate(BaseModel):
    user_name: str

class RegistrationResponse(BaseModel):
    id: int
    event_id: int
    user_name: str
    registered_at: datetime
    is_cancelled: bool

    class Config:
        from_attributes = True