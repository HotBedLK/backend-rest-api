from fastapi import HTTPException,status

class GeneralUserExceptions(Exception):
    def __init__(
        self,
        error_code: str,
        error_message: str,
        status_code: int = 400,
    ):
        self.error_code = error_code
        self.error_message = error_message
        self.status_code = status_code


class SupabaseApiFailException(GeneralUserExceptions):
    def __init__(self, message: str):
        super().__init__(
            error_code="INTERNAL_SERVER_ERROR",
            error_message=message,
            status_code=500,
        )


class NotAcceptablePostIDException(GeneralUserExceptions):
    def __init__(self, message: str):
        super().__init__(
            error_code="NOT_ACCEPTABLE_POST_ID",
            error_message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

class NotExsistPropertyException(GeneralUserExceptions):
    def __init__(self, message: str):
        super().__init__(
            error_code="PROPERTY_NOT_EXIST",
            error_message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class GeneralUserServiceLayerException(GeneralUserExceptions):
    def __init__(self, message: str):
        super().__init__(
            error_code="INTERNAL_SERVER_ERROR",
            error_message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )







class GeneralUserCacheStorageException(GeneralUserExceptions):
    def __init__(self, message: str):
        super().__init__(
            error_code="INTERNAL_SERVER_ERROR",
            error_message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )





