# purpose : verify mobile number ( purpose is change password on provide account or verify account )
# input data 
# mobile number
# OTP

from fastapi import APIRouter,Depends
from supabase import Client
from typing import Annotated
from app.database.supabase import get_supabase_client
from ..services.verifyMobileNumberService import verifyMobileNumberService
from app.database.supabase import get_supabase_client
from ..schemas.verifyMobileNumberSchema import VerifyMobileNumberSchema
from app.utils.rate_limiter import RateLimiter


router_login  = APIRouter(tags=["Login Routes"])

@router_login.post('/verify_mobile_number',description="verify mobile number using otp for password-change or verify account")
async def verifyMobileNumber(data : VerifyMobileNumberSchema, 
                              db : Annotated[Client, Depends(get_supabase_client)],
                              _: Annotated[None, Depends(RateLimiter(limit=5, window_seconds=60, key_prefix="register"))],
                              ):
    return verifyMobileNumberService(data, db)