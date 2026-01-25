from fastapi import APIRouter, Depends
from typing import Annotated
from supabase import  Client
from app.database.supabase import get_supabase_client
from app.services.jwt import authVerification
from services.SubscriptionService.app.services.SubscriptionService import CreateSubscriptionService
from services.SubscriptionService.app.schemas.SubscriptionScheme import CreateSubscriptionResponse

router = APIRouter(tags=["Subscription service"])


## NOTE This function is used for create subscription on to a user
@router.post("/create", description="used for create subscription on to a user",response_model=CreateSubscriptionResponse)
def CreateSubscriptionControlelr(db: Annotated[Client, Depends(get_supabase_client)]):
    # user_details: Annotated[dict, Depends(authVerification)],
    DUMMY_USER_UNTILL_FIX_LOGIN_AUTH  = "3a1dfef2-cc77-4b61-bcfc-030a389f124d"
    order_id = CreateSubscriptionService(db=db,user_id=DUMMY_USER_UNTILL_FIX_LOGIN_AUTH)
    return CreateSubscriptionResponse(order_id=order_id)


