from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Event
from schemas import EventCreate, EventResponse
from datetime import datetime
from typing import List

router = APIRouter()

@router.post("/events", response_model=EventResponse)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    # Check if event name already exists
    existing = db.query(Event).filter(Event.name == event.name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Event name already exists")
    
    # Check if date is in the future
    if event.date <= datetime.utcnow():
        raise HTTPException(status_code=400, detail="Event date must be in the future")
    
    # Check if seats are greater than 0
    if event.total_seats <= 0:
        raise HTTPException(status_code=400, detail="Total seats must be greater than 0")
    
    new_event = Event(
        name=event.name,
        date=event.date,
        total_seats=event.total_seats,
        available_seats=event.total_seats
    )
    
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@router.get("/events", response_model=List[EventResponse])
def get_events(upcoming_only: bool = False, db: Session = Depends(get_db)):
    query = db.query(Event)
    
    if upcoming_only:
        query = query.filter(Event.date >= datetime.utcnow())
    
    events = query.order_by(Event.date).all()
    return events