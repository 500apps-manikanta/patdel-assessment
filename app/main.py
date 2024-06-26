from fastapi import FastAPI
from app.routers import accounts, destinations, data_handler

app = FastAPI()

app.include_router(accounts.router, prefix="/accounts", tags=["Accounts"])
app.include_router(destinations.router, prefix="/destinations", tags=["Destinations"])
app.include_router(data_handler.router, prefix="/server", tags=["Webhook"])
