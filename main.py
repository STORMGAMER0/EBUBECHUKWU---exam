from fastapi import FastAPI

from database import Speaker
from routes.event import event_router
from routes.user import user_router
from routes.registration import registration_router

app = FastAPI()
app.include_router(user_router, tags=["User"])
app.include_router(event_router, tags=["Event"])
app.include_router(registration_router, tags=["Registration"])

@app.get("/speakers")
def get_speakers():
    return Speaker