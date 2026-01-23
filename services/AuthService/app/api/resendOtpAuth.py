from fastapi import APIRouter, Depends
from supabase import Client
from typing import Annotated

from app.database.supabase import get_supabase_client
from app.utils.rate_limiter import RateLimiter
from ..schemas.resendOtpInputSchema import ResendOtpInputSchema
from ..services.resendOtpService import resend_otp_service


router = APIRouter(tags=["Auth Routes"])


@router.post("/resend-otp", description="resend otp code")
def resend_otp(
    data: ResendOtpInputSchema,
    db: Annotated[Client, Depends(get_supabase_client)],
    _: Annotated[None, Depends(RateLimiter(limit=5, window_seconds=60, key_prefix="resend-otp"))],
):
    return resend_otp_service(resend_data=data.model_dump(), db=db)
