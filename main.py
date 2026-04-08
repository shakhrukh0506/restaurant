from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from restaurant.api import api_router

app = FastAPI(title="Restaurant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)