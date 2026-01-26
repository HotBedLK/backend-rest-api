from pydantic import BaseModel,Field,field_validator,EmailStr,SecretStr,HttpUrl
from typing import Optional
from datetime import datetime



class CreateSubscriptionResponse(BaseModel):
    """
    response for create subscription
    """
    order_id:str = Field(...,example="SUB-20240128-ABC123")
    status:str = Field(default="succuss")
    message:str = Field(default="subscription created! waiting for payemnt triggers")



##* schema for the payment initiate controller
##! required order id
class InitiateSubscription(BaseModel):
    order_id:str = Field(...,examples=["ORD-XXXX-XXXX"],description="recived order if from previous trigger")

    @field_validator("order_id")
    @classmethod
    def order_id_validator(cls,value:str):
        if len(value) < 1:
            raise ValueError("order id cannot be empty")
        if not value.startswith("ORD"):
            raise ValueError("invalid order id")
        return value
    

#! initiate payment models
class DatabaseUserModel(BaseModel):
    email: str
    last_name: str
    first_name: str
    mobile_number: str

class DatabaseSubscriptionModel(BaseModel):
    id: str
    created_at: datetime
    user_id: str
    order_id: str
    status: str
    started_at: Optional[datetime]
    valid_until: Optional[datetime]
    amount: Optional[int]
    currency: str
    last_payment_id: Optional[str]
    Users: DatabaseUserModel  


class InitiatePaymentModel(BaseModel):
    """
    Model for sending payment data to frontend
    """
    merchant_id: str = Field(..., description="Your PayHere Merchant ID")
    order_id: str = Field(..., description="Order ID from database")
    amount: str = Field(default="500.00", description="Always 500 LKR")
    currency: str = Field(default="LKR", description="Currency")
    
    # User info from database Users object
    first_name: str = Field(..., description="From database Users.first_name")
    last_name: str = Field(..., description="From database Users.last_name")
    email: EmailStr = Field(..., description="From database Users.email")
    phone: str = Field(..., description="From database Users.mobile_number")
    address: str = Field(default="12/b kohuwala", description="Default address")
    city: str = Field(default="colombo", description="Default city")
    country: str = Field(default="Sri Lanka", description="Default country")
    return_url: HttpUrl = Field(..., description="Where user goes after payment")
    cancel_url: HttpUrl = Field(..., description="Where user goes if cancels")
    notify_url: HttpUrl = Field(..., description="PayHere webhook URL")
    
    hash: str = Field(..., description="Generated hash for payhere")

# Helper function to map database result to payment model
def create_payment_model(
    db_subscription: DatabaseSubscriptionModel,
    merchant_id: str,
    hash_value: str,
    return_url: str,
    cancel_url: str,
    notify_url: str
) -> InitiatePaymentModel:
    """
    Convert database subscription to payment model for frontend
    """
    
    return InitiatePaymentModel(
        merchant_id=merchant_id,
        order_id=db_subscription.order_id,
        amount="500.00",
        currency=db_subscription.currency or "LKR",
        first_name=db_subscription.Users.first_name,
        last_name=db_subscription.Users.last_name,
        email=db_subscription.Users.email,
        phone=db_subscription.Users.mobile_number,
        return_url=return_url,
        cancel_url=cancel_url,
        notify_url=notify_url,
        hash=hash_value
    )
