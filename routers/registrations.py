from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Event, Registration
from schemas import RegistrationCreate, RegistrationResponse
from datetime import datetime

router = APIRouter()

@router.post("/events/{event_id}/register", response_model=RegistrationResponse)
def register_user(event_id: int, registration: RegistrationCreate, db: Session = Depends(get_db)):
    
    # Lock the event row to prevent race conditions
    event = db.query(Event).filter(Event.id == event_id).with_for_update().first()
    
    # Check if event exists
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check if event is in the future
    if event.date <= datetime.utcnow():
        raise HTTPException(status_code=400, detail="Event has already passed")
    
    # Check for available seats
    if event.available_seats <= 0:
        raise HTTPException(status_code=400, detail="No available seats")
    
    # Check for duplicate registration
    existing = db.query(Registration).filter(
        Registration.event_id == event_id,
        Registration.user_name == registration.user_name,
        Registration.is_cancelled == False
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="User already registered for this event")
    
    # Create registration
    new_registration = Registration(
        event_id=event_id,
        user_name=registration.user_name,
    )
    
    # Decrease available seats
    event.available_seats -= 1
    
    db.add(new_registration)
    db.commit()
    db.refresh(new_registration)
    return new_registration


@router.delete("/events/{event_id}/registrations/{registration_id}", response_model=RegistrationResponse)
def cancel_registration(event_id: int, registration_id: int, db: Session = Depends(get_db)):
    
    # Lock the event row
    event = db.query(Event).filter(Event.id == event_id).with_for_update().first()
    
    # Check if event exists
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Find the registration
    registration = db.query(Registration).filter(
        Registration.id == registration_id,
        Registration.event_id == event_id
    ).first()

    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")

    # Check if already cancelled
    if registration.is_cancelled:
        raise HTTPException(status_code=400, detail="Registration is already cancelled")

    # Cancel the registration and restore the seat
    registration.is_cancelled = True
    event.available_seats += 1

    db.commit()
    db.refresh(registration)
    return registration