import os
from functools import lru_cache

from dotenv import load_dotenv
from supabase import Client, create_client
from decouple import config



@lru_cache(maxsize=1)
def get_supabase_client() -> Client:
    supabase_url = config("SUPABASE_URL")
    supabase_key = config("SUPABASE_SERVICE_ROLE_KEY") or config("SUPABASE_ANON_KEY")

    if not supabase_url or not supabase_key:
        raise RuntimeError(
            "Supabase config missing: set SUPABASE_URL and "
            "SUPABASE_SERVICE_ROLE_KEY (or SUPABASE_ANON_KEY)."
        )
    

    return create_client(supabase_url, supabase_key)
