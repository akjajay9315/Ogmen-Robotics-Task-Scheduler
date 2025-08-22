from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <--- import CORS
from .routers import devices, tasks, logs
from . import models, database

app = FastAPI(title="ORo Task Scheduler API", version="1.0.0")

# ------------------- CORS Setup -------------------
origins = [
    "http://localhost:5500",  # frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # allow frontend
    allow_credentials=True,
    allow_methods=["*"],        # allow GET, POST, PUT, DELETE
    allow_headers=["*"],        # allow all headers
)
# ---------------------------------------------------

# include routers
app.include_router(devices.router)
app.include_router(tasks.router)
app.include_router(logs.router)
