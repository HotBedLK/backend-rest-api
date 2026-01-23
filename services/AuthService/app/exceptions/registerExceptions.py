from fastapi import HTTPException

class RegisterException(Exception):
    def __init__(
        self,
        error_code: str,
        error_message: str,
        status_code: int = 400,
    ):
        self.error_code = error_code
        self.error_message = error_message
        self.status_code = status_code



class SupabaseApiFailException(RegisterException):
    def __init__(self, message: str):
        super().__init__(
            error_code="INTERNAL_SERVER_ERROR",
            error_message=message,
            status_code=500,
        )


class SmsGatewayException(RegisterException):
    def __init__(self, message: str):
        super().__init__(
            error_code="SMS_GATEWAY_ERROR",
            error_message=message,
            status_code=502,
        )


class SmsGatewayConfigException(RegisterException):
    def __init__(self, message: str):
        super().__init__(
            error_code="SMS_GATEWAY_CONFIG_ERROR",
            error_message=message,
            status_code=500,
        )


class InvalidMobileNumberException(RegisterException):
    def __init__(self, message: str):
        super().__init__(
            error_code="INVALID_MOBILE_NUMBER",
            error_message=message,
            status_code=422,
        )


class InvalidOtpException(RegisterException):
    def __init__(self, message: str):
        super().__init__(
            error_code="INVALID_OTP",
            error_message=message,
            status_code=422,
        )


class UserNotFoundException(RegisterException):
    def __init__(self, message: str):
        super().__init__(
            error_code="USER_NOT_FOUND",
            error_message=message,
            status_code=404,
        )


class UserAlreadyVerifiedException(RegisterException):
    def __init__(self, message: str):
        super().__init__(
            error_code="USER_ALREADY_VERIFIED",
            error_message=message,
            status_code=409,
        )


class OtpExpiredException(RegisterException):
    def __init__(self, message: str):
        super().__init__(
            error_code="OTP_EXPIRED",
            error_message=message,
            status_code=410,
        )


class ResendOtpLimitException(RegisterException):
    def __init__(self, message: str):
        super().__init__(
            error_code="OTP_RESEND_LIMIT",
            error_message=message,
            status_code=429,
        )


class ResendOtpCooldownException(RegisterException):
    def __init__(self, message: str):
        super().__init__(
            error_code="OTP_RESEND_COOLDOWN",
            error_message=message,
            status_code=429,
        )


class UserEmailAlreadyExistsException(RegisterException):
    def __init__(self, message: str):
        super().__init__(
            error_code="DUPLICATE_USER_CREATION",
            error_message=message,
            status_code=401,
        )


class UserNumberAlreadyExistsException(RegisterException):
    def __init__(self, message: str):
        super().__init__(
            error_code="DUPLICATE_USER_CREATION",
            error_message=message,
            status_code=401,
        )

class credencialsNotMatchedException(RegisterException):
    def __init__(self, message: str):
        super().__init__(
            error_code="CREDENCIALS_NOT_MATCHED",
            error_message=message,
            status_code=401,
        )

class databaseUpdateFaildException(RegisterException):
    def __init__(self, message: str):
        super().__init__(
            error_code="DATABASE_UPDATE_FAILD",
            error_message=message,
            status_code=500,
        )

class vefiricationCodeNotFoundException(RegisterException):
    def __init__(self, message: str):
        super().__init__(
            error_code="VEFIRICATION_CODE_NOT_FOUND",
            error_message=message,
            status_code=404,
        )

class userNotAllowedToModified(RegisterException):
    def __init__(self, message: str):
        super().__init__(
            error_code="USER_NOT_ALLOWED_TO_MODIFIED",
            error_message=message,
            status_code=403,
        )