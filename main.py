from fastapi import FASTapi
from fastapi.middleware.cors import CORSMiddleware

app = FASTapi()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
