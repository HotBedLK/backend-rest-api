from fastapi import APIRouter, Depends
from supabase import Client
from typing import Annotated
from app.database.supabase import get_supabase_client
from app.utils.rate_limiter import RateLimiter
from ..exceptions import registerExceptions
from ..schemas.registerInputSchema import RegisterInputSchema
from ..services.registerService import registerService


router  = APIRouter(tags=["Auth Routes"])

@router.post("/",description="register a user in the system")
def register(
    data: RegisterInputSchema,
    db: Annotated[Client, Depends(get_supabase_client)],
    _: Annotated[None, Depends(RateLimiter(limit=5, window_seconds=60, key_prefix="register"))],
):
    return registerService(registerData=data.model_dump(),db=db)
