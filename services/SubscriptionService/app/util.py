import uuid
from datetime import datetime


def CreateOrderId(prefix="SUB"):
    """    
    :param prefix: what type of order id
    this function is used to create unique order id for the orders 
    """
    unique_part = uuid.uuid4().hex[:8].upper()
    date_time_part = datetime.now().strftime("%Y%m%d")
    return f"{prefix}-{date_time_part}-{unique_part}"

