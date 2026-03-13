from fastapi import APIRouter, Depends
from typing import Annotated
from supabase import  Client
from app.database.supabase import get_supabase_client
from app.services.jwt import authVerification
from services.SubscriptionService.app.services.SubscriptionService import CreateSubscriptionService
from services.SubscriptionService.app.schemas.SubscriptionScheme import (
  CreateSubscriptionResponse, InitiateSubscription)
from services.SubscriptionService.app.services.InitiatePaymentService import initiate_payment

router = APIRouter(tags=["Subscription service"])


##* NOTE This function is used for create subscription on to a user
#? this controller task is create partial order record in the databse table. after payment sucuuss we are up
#?date the record with succiss states. for now its in pending state
@router.post("/create", description="used for create subscription on to a user",response_model=CreateSubscriptionResponse)
def CreateSubscriptionControlelr(db: Annotated[Client, Depends(get_supabase_client)]):
    # user_details: Annotated[dict, Depends(authVerification)],
    DUMMY_USER_UNTILL_FIX_LOGIN_AUTH  = "3a1dfef2-cc77-4b61-bcfc-030a389f124d"
    order_id = CreateSubscriptionService(db=db,user_id=DUMMY_USER_UNTILL_FIX_LOGIN_AUTH)
    return CreateSubscriptionResponse(order_id=order_id)


##* NOTE this functio is used for generate payhere hook for send to the frontend
#? why this ? because of some users are closethe web page after seeing subscription price. from this we 
#? are getting actual order id and its atatus. in the frontend must be manage the state
@router.post("/initiate",description="this controller is used to return payment gateway frontend hook")
def InitiatePayment(db: Annotated[Client,Depends(get_supabase_client)],order_id:InitiateSubscription):
    return initiate_payment(db=db,order_id=order_id.model_dump().get("order_id"))
