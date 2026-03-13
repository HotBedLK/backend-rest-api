import uuid
from datetime import datetime
from services.SubscriptionService.app.schemas.SubscriptionScheme import (create_payment_model,
  DatabaseSubscriptionModel)
from decouple import config
from hashlib import md5
from services.AuthService.app.util import hash_otp_code

PAYHERE_MERCHENT_ID = config("PAYHERE_MERCHENT_ID")
FRONTEND_CANCEL_URL = config("FRONTEND_CANCEL_URL")
FRONTEND_RETURN_URL= config("FRONTEND_RETURN_URL")
PAYHERE_WEBHOOK_URL =  config("WEBHOOK_URL_PAYHERE")
PAYHERE_MERCHENT_SECRET = config("PAYHERE_MERCHENT_SECRET")


def CreateOrderId(prefix="SUB"):
    """    
    :param prefix: what type of order id
    this function is used to create unique order id for the orders 
    """
    unique_part = uuid.uuid4().hex[:8].upper()
    date_time_part = datetime.now().strftime("%Y%m%d")
    return f"{prefix}-{date_time_part}-{unique_part}"


import hashlib

def generate_payhere_hash(order_id: str, amount: str, currency: str) -> str:
    """
    Generate PayHere hash
    Format: hash = md5(merchant_id + order_id + amount + currency + md5(merchant_secret))
    """
    hashed_secret = hashlib.md5(
        PAYHERE_MERCHENT_SECRET.encode() 
    ).hexdigest().upper() 
    
    if "." not in amount:
        amount = f"{float(amount):.2f}"
    
    hash_string = (
        PAYHERE_MERCHENT_ID +
        order_id +
        amount +  
        currency +
        hashed_secret 
    )
    final_hash = hashlib.md5(
        hash_string.encode() 
    ).hexdigest().upper()  

    return final_hash



def create_payment_response_model(order):
    """
    this function gets row database data object and convert it to pydantic data model to sent frontend
    :param order: valid order
    """
    subscription_data = DatabaseSubscriptionModel(**order["data"][0])
    return create_payment_model(
      db_subscription=subscription_data,
      merchant_id=PAYHERE_MERCHENT_ID,
      hash_value="",
      return_url=FRONTEND_RETURN_URL,
      cancel_url=FRONTEND_CANCEL_URL,
      notify_url=PAYHERE_WEBHOOK_URL,
    )

