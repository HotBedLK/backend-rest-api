from pydantic import BaseModel, Field, field_validator

class VerifyMobileNumberSchema(BaseModel):
    mobile_number: str = Field(
        ...,
        description="Mobile number must be 10 digits",
        examples=["0767722791"],
    )
    otp : int = Field(
        ...,
        description="OTP code sent to the mobile number",
        examples=[123456],
    )

    @field_validator("mobile_number")
    def validate_mobile_number(cls, value):
        if not value.isdigit():
            raise ValueError("Mobile number must contain only digits")
        if len(value) != 10:
            raise ValueError("Mobile number must be exactly 10 digits")
        return value
    
    @field_validator("otp")
    def validate_otp(cls, value):
        if not (100000 <= value <= 999999):
            raise ValueError("OTP must be a 6-digit number")
        return value