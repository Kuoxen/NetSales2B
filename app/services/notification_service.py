from typing import Dict, Any
import asyncio
from datetime import datetime

class NotificationService:
    def __init__(self):
        self.active_listeners = set()
    
    async def notify_reply_received(self, merchant_id: int, message: str):
        """通知有客户回复，需要人工接手"""
        notification = {
            "type": "merchant_reply",
            "merchant_id": merchant_id,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "priority": "high"
        }
        
        # Send to all active listeners (WebSocket connections)
        await self._broadcast_notification(notification)
        
        # Send to external notification systems (企业微信/钉钉)
        await self._send_external_notification(notification)
    
    async def _broadcast_notification(self, notification: Dict[str, Any]):
        """广播通知到所有WebSocket连接"""
        if self.active_listeners:
            # Implementation for WebSocket broadcasting
            print(f"Broadcasting notification: {notification}")
    
    async def _send_external_notification(self, notification: Dict[str, Any]):
        """发送到外部通知系统"""
        # Implementation for external notifications
        print(f"External notification: {notification}")
    
    def add_listener(self, listener_id: str):
        self.active_listeners.add(listener_id)
    
    def remove_listener(self, listener_id: str):
        self.active_listeners.discard(listener_id)