from fastapi import APIRouter, Depends
from supabase import Client
from typing import Annotated

from app.database.supabase import get_supabase_client
from app.utils.rate_limiter import RateLimiter
from ..schemas.verifyInputSchema import VerifyInputSchema
from ..services.verifyService import verify_service


router = APIRouter(tags=["Auth Routes"])


@router.post("/verify", description="verify account with otp")
def verify_account(
    data: VerifyInputSchema,
    db: Annotated[Client, Depends(get_supabase_client)],
    _: Annotated[None, Depends(RateLimiter(limit=5, window_seconds=60, key_prefix="verify"))],
):
    return verify_service(verify_data=data.model_dump(), db=db)
