from abc import ABC, abstractmethod
from playwright.async_api import async_playwright
from typing import List, Dict
import asyncio

class BaseScraper(ABC):
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser = None
        self.page = None
    
    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.page = await self.browser.new_page()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    @abstractmethod
    async def scrape_merchants(self, filters: Dict) -> List[Dict]:
        pass
    
    async def delay(self, seconds: float = 1.0):
        await asyncio.sleep(seconds)