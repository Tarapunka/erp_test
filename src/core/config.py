from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "ERP_API"
    debug: bool = True
    database_url: str = "sqlite+aiosqlite:///./erp.db"
    secret_key: str = "mysupersecretkey"
    algorithm: str = "HS256"
    access_expire_token_min: int = 15
    refresh_expire_days: int = 7
    refresh_secret_key: str = "refresh-secret-key"

    class Config:
        env_file = ".env"

settings = Settings()
