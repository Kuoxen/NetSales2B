from .celery_app import celery_app
from app.scrapers.fastmoss import FastmossScraper

@celery_app.task
async def scrape_merchants_task(filters: dict):
    """异步抓取商家数据任务"""
    async with FastmossScraper() as scraper:
        merchants = await scraper.scrape_merchants(filters)
    return merchants

@celery_app.task
def schedule_daily_scraping():
    """定时任务：每日数据抓取"""
    filters = {
        "platform": "tiktok_shop",
        "region": "southeast_asia",
        "max_gmv": 1000000
    }
    return scrape_merchants_task.delay(filters)