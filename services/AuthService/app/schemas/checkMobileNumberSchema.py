from pydantic import BaseModel, Field, field_validator

class CheckMobileNumberSchema(BaseModel):
    mobile_number: str = Field(
        description="Mobile number used for registration (10 digits starting with 0). this is only use sri lankan mobile number",
        examples=["0767722791"],
    )

    @field_validator("mobile_number")
    def validate_mobile_number(cls, value):
        if value is None:
            return ValueError("Mobile number is required")
        if not value.isdigit():
            raise ValueError("Mobile number must contain only digits")
        if len(value) != 10 or not value.startswith("0"):
            raise ValueError("Mobile number must be 10 digits starting with 0")
        return value