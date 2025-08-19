from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class PlatformType(enum.Enum):
    TIKTOK_SHOP = "tiktok_shop"
    LAZADA = "lazada"
    SHOPEE = "shopee"

class ContactStatus(enum.Enum):
    PENDING = "pending"
    CONTACTED = "contacted"
    REPLIED = "replied"
    CONVERTED = "converted"
    REJECTED = "rejected"

class Merchant(Base):
    __tablename__ = "merchants"
    
    id = Column(Integer, primary_key=True)
    shop_name = Column(String, nullable=False)
    platform = Column(Enum(PlatformType), nullable=False)
    shop_url = Column(String, unique=True)
    contact_info = Column(String)
    gmv_usd = Column(Float)
    region = Column(String)
    contact_status = Column(Enum(ContactStatus), default=ContactStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    contacted_at = Column(DateTime)
    last_reply_at = Column(DateTime)