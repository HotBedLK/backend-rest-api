from fastapi import HTTPException,status

class SubscriptionExceptions(Exception):
    def __init__(
        self,
        error_code: str,
        error_message: str,
        status_code: int = 400,
    ):
        self.error_code = error_code
        self.error_message = error_message
        self.status_code = status_code



class SupabaseApiFailException(SubscriptionExceptions):
    def __init__(self, message: str):
        super().__init__(
            error_code="INTERNAL_SERVER_ERROR",
            error_message=message,
            status_code=500,
        )


class CreateSubscriptionException(SubscriptionExceptions):
    def __init__(self, message: str):
        super().__init__(
            error_code="INTERNAL_SERVER_ERROR",
            error_message=message,
            status_code=500,
        )

class InitiatePaymentSubscriptionException(SubscriptionExceptions):
    def __init__(self, message: str,error_code:str,status_code:int):
        super().__init__(
            error_code=error_code,
            error_message=message,
            status_code=status_code,
        )



