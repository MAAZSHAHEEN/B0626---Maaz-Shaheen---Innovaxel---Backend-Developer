from fastapi import FastAPI
from database import engine, Base
from routers import events, registrations

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(events.router)
app.include_router(registrations.router)