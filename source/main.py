from fastapi import FastAPI, Depends, HTTPException, status, Response
from .database import get_db, engine
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .routers import post, user, auth
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)


origins = ["http://localhost", "http://localhost:8000", "http://127.0.0.1:8000"]


app = FastAPI()

origins = [
    "http://localhost:3000",  # Adjust depending on where your frontend is hosted
    "http://localhost:8000",  # Example of another local frontend port
    "http://127.0.0.1:8000",  # Example if using Live Server in VSCode
]

# Add CORS middleware to allow the specified origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow credentials, methods, and headers for these origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods, or specify e.g., ["GET", "POST"]
    allow_headers=["*"],  # Allow all headers, or be specific e.g., ["Content-Type"]
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"Hello": "World"}
