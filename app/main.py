from fastapi import FastAPI
from app.api import merchants, campaigns, notifications
from app.core.config import settings

app = FastAPI(title="NetSales2B", version="1.0.0")

app.include_router(merchants.router, prefix="/api/merchants", tags=["merchants"])
app.include_router(campaigns.router, prefix="/api/campaigns", tags=["campaigns"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["notifications"])

@app.get("/")
async def root():
    return {"message": "NetSales2B API"}