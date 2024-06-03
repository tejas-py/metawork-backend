from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from routers import *
from connection.database import engine
from models import user_model

# Configure app
app = FastAPI()
user_model.Base.metadata.create_all(bind=engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Register the blueprint with a custom URL prefix
app.include_router(
    users.user_router,
    prefix="/user"
)


@app.get("/")
async def home_page():
    return RedirectResponse("https://www.facebook.com", status_code=302)
