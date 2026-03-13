# purpose : change password on account
# step : this is only allow to change once the 'password change' OTP verified
# input data 
# mobile number
# new password

from fastapi import APIRouter,Depends
from supabase import Client
from typing import Annotated
from app.database.supabase import get_supabase_client
from ..services.changePasswordService import changePasswordService
from ..schemas.changePasswordSchema import changePasswordSchema
from app.utils.rate_limiter import RateLimiter


router_login  = APIRouter(tags=["Login Routes"])
@router_login.post('/change_password',description="change user password after the email verification")
async def change_password(
    data: changePasswordSchema,
    db: Annotated[Client, Depends(get_supabase_client)],
    # _: Annotated[None, Depends(RateLimiter(limit=5, window_seconds=60, key_prefix="register"))],
    ):
    return changePasswordService(data=data, db=db)