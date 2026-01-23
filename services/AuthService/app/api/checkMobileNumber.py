from fastapi import APIRouter,Depends
from supabase import Client
from typing import Annotated
from app.database.supabase import get_supabase_client
from ..services.checkMobileNumberService import checkMobileNumber
from app.database.supabase import get_supabase_client
from ..schemas.checkMobileNumberSchema import CheckMobileNumberSchema
from app.utils.rate_limiter import RateLimiter


router_login  = APIRouter(tags=["Login Routes"])

@router_login.post('/check_mobile_number',description="verify mobile number on the database")
async def check_mobile_number(data : CheckMobileNumberSchema, 
                              db : Annotated[Client, Depends(get_supabase_client)],
                              _: Annotated[None, Depends(RateLimiter(limit=5, window_seconds=60, key_prefix="register"))],
                              ):
    return checkMobileNumber(data, db)
