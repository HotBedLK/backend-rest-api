from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


class ResendOtpInputSchema(BaseModel):
    email: EmailStr | None = Field(
        default=None,
        description="Email address used for registration",
        examples=["user@example.com"],
    )
    mobile_number: str | None = Field(
        default=None,
        description="Mobile number used for registration (10 digits starting with 0)",
        examples=["0767722791"],
    )

    @field_validator("mobile_number")
    def validate_mobile_number(cls, value):
        if value is None:
            return value
        if not value.isdigit():
            raise ValueError("Mobile number must contain only digits")
        if len(value) != 10 or not value.startswith("0"):
            raise ValueError("Mobile number must be 10 digits starting with 0")
        return value

    @model_validator(mode="after")
    def require_email_or_mobile(self):
        if not self.email and not self.mobile_number:
            raise ValueError("Either email or mobile_number is required")
        return self
