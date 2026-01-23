from pydantic import BaseModel, Field, field_validator


class changePasswordSchema(BaseModel):
    mobile_number: str = Field(
        ...,
        description="User's mobile number",
        examples=["0771234567"]
    )   
    password : str = Field(
        ...,
        description="New password for the user account",
        examples=["NewStrongPassword123!"]
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
    
    @field_validator("password")
    def validate_password(cls, value):
        if value is None:
            raise ValueError("Password is required")
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return value