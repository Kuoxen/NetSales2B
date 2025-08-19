from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.notification_service import NotificationService

router = APIRouter()
notification_service = NotificationService()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket连接用于实时通知"""
    await websocket.accept()
    listener_id = f"ws_{id(websocket)}"
    notification_service.add_listener(listener_id)
    
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        notification_service.remove_listener(listener_id)

@router.post("/reply")
async def handle_merchant_reply(merchant_id: int, message: str):
    """处理商家回复"""
    await notification_service.notify_reply_received(merchant_id, message)
    return {"status": "notification_sent"}