from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from app.scrapers.fastmoss import FastmossScraper
from app.services.contact_service import ContactService

router = APIRouter()

@router.post("/scrape")
async def scrape_merchants(filters: Dict):
    """从数据源抓取商家信息"""
    async with FastmossScraper() as scraper:
        merchants = await scraper.scrape_merchants(filters)
    
    return {"merchants": merchants, "count": len(merchants)}

@router.post("/contact")
async def contact_merchants(merchant_ids: List[int]):
    """批量联系商家"""
    contact_service = ContactService()
    # Get merchants from database by IDs
    # merchants = get_merchants_by_ids(merchant_ids)
    
    # results = await contact_service.batch_contact_merchants(merchants)
    results = {"success": 0, "failed": 0, "skipped": 0}  # Placeholder
    
    return results

@router.get("/")
async def list_merchants(skip: int = 0, limit: int = 100):
    """获取商家列表"""
    # Implementation for listing merchants from database
    return {"merchants": [], "total": 0}