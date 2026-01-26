from services.SubscriptionService.app.util import CreateOrderId
from services.SubscriptionService.app.exceptions.SubscriptionExceptions import (
    CreateSubscriptionException)
from services.SubscriptionService.app.db.subscription_db import subscription



def CreateSubscriptionService(db,user_id)->bool:
    """
    :param user_email: str
    :return bool
    """
    #generate order id
    order_id = CreateOrderId(prefix="ORD") #ORD prefix use for create id for order 
    #call the transaction layer for transaction
    try:
        ord = subscription.CreateSubscriptionRepoFunc(db=db,user_id=user_id,order_id=order_id)
        if ord is not None:
            return ord
        raise CreateSubscriptionException(message="transactional error!")
    except CreateSubscriptionException:
        raise
    except Exception as e:
        print("something happened in CreateSubscriptionService function",e)

