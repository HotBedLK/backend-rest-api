from pydantic import BaseModel,Field


class CreateSubscriptionResponse(BaseModel):
    """
    response for create subscription
    """
    order_id:str = Field(...,example="SUB-20240128-ABC123")
    status:str = Field(default="succuss")
    message:str = Field(default="subscription created! waiting for payemnt triggers")

