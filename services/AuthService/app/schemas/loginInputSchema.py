from pydantic import BaseModel, field_validator


class LoginInputSchema(BaseModel):
    mobile_number: str
    password: str

    @field_validator("mobile_number")
    def validate_mobile_number(cls, value):
        if not value.isdigit():
            raise ValueError("Mobile number must contain only digits")
        if len(value) != 10 or not value.startswith("0"):
            raise ValueError("Mobile number must be 10 digits starting with 0")
        return value
    
    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 6 characters long")
        return value