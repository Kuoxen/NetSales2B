from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://user:password@localhost/netsales2b"
    redis_url: str = "redis://localhost:6379"
    secret_key: str = "your-secret-key"
    
    # Scraping settings
    max_concurrent_scrapers: int = 5
    scraping_delay: float = 1.0
    
    # Contact settings
    max_daily_contacts: int = 1000
    
    class Config:
        env_file = ".env"

settings = Settings()