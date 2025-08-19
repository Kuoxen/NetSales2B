from fastapi import APIRouter
from typing import Dict

router = APIRouter()

@router.post("/")
async def create_campaign(campaign_data: Dict):
    """创建营销活动"""
    return {"message": "Campaign created", "id": 1}

@router.get("/{campaign_id}")
async def get_campaign(campaign_id: int):
    """获取活动详情"""
    return {"id": campaign_id, "status": "active"}

@router.get("/{campaign_id}/stats")
async def get_campaign_stats(campaign_id: int):
    """获取活动统计"""
    return {
        "contacted": 100,
        "replied": 15,
        "converted": 3,
        "response_rate": 0.15
    }