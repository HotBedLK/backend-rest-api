
from fastapi import status
from services.SubscriptionService.app.db.subscription_db import subscription
from services.SubscriptionService.app.exceptions.SubscriptionExceptions import ( InitiatePaymentSubscriptionException)
from services.SubscriptionService.app.util import (create_payment_response_model,
  generate_payhere_hash)





def initiate_payment(db,order_id:str):
  """
  This function is used for getting order record from the database with order id with help
  of repo layer and return it to the controller
  
  :param db: supabase d instance
  :param order_id: valid order id
  :type order_id: str
  """
  order = subscription.GetSubscription(db=db,order_id=order_id)
  if not order["status"]:
    raise InitiatePaymentSubscriptionException(
      message=order["reason"],
      error_code="INVALID_ORDER_ID",
      status_code=status.HTTP_400_BAD_REQUEST
    ) 
  model =  create_payment_response_model(order=order)
  print(model)
  hash = generate_payhere_hash(order_id=model.order_id,amount=model.amount,currency=model.currency)
  model.hash = hash
  return model
  
