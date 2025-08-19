from typing import List
from app.models.merchant import Merchant, ContactStatus
from app.core.config import settings
import asyncio

class ContactService:
    def __init__(self):
        self.daily_contact_count = 0
        self.max_daily_contacts = settings.max_daily_contacts
    
    async def batch_contact_merchants(self, merchants: List[Merchant]) -> dict:
        results = {"success": 0, "failed": 0, "skipped": 0}
        
        for merchant in merchants:
            if self.daily_contact_count >= self.max_daily_contacts:
                results["skipped"] += 1
                continue
            
            try:
                success = await self._contact_merchant(merchant)
                if success:
                    merchant.contact_status = ContactStatus.CONTACTED
                    results["success"] += 1
                    self.daily_contact_count += 1
                else:
                    results["failed"] += 1
                
                # Rate limiting
                await asyncio.sleep(settings.scraping_delay)
                
            except Exception as e:
                print(f"Error contacting merchant {merchant.id}: {e}")
                results["failed"] += 1
        
        return results
    
    async def _contact_merchant(self, merchant: Merchant) -> bool:
        # Implementation for contacting merchant
        # This would integrate with WhatsApp/Telegram/Email APIs
        print(f"Contacting merchant: {merchant.shop_name}")
        return True