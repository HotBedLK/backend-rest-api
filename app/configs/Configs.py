from pydantic_settings import BaseSettings
from decouple import config


class Settings(BaseSettings):
    SUPABASE_URL:str = config("SUPABASE_URL")
    SUPABASE_SERVICE_ROLE_KEY:str = config("SUPABASE_SERVICE_ROLE_KEY")
    SUPABASE_ANON_KEY:str = config("SUPABASE_ANON_KEY")


def get_settings():
    settings = Settings()
    return settings
