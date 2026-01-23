from datetime import datetime, timezone

from ..db.transactions import Transactions
from app.utils.rate_limiter import get_redis_client
from ..exceptions.registerExceptions import (
    InvalidOtpException,
    OtpExpiredException,
    UserAlreadyVerifiedException,
    UserNotFoundException,
)
from ..util import hash_otp_code, is_otp_expired, is_timestamp_expired


def verify_service(verify_data, db):
    if verify_data.get("email"):
        user = Transactions.get_user_for_verification_by_email(
            email=verify_data["email"], db=db
        )
    else:
        user = Transactions.get_user_for_verification_by_mobile(
            number=verify_data["mobile_number"], db=db
        )

    if not user:
        raise UserNotFoundException(message="User not found.")

    if user.get("verified"):
        raise UserAlreadyVerifiedException(message="User already verified.")

    latest_attempt = Transactions.get_latest_otp_attempt(user_id=user["id"], db=db)
    if latest_attempt:
        if is_timestamp_expired(latest_attempt["expires_at"]):
            raise OtpExpiredException(message="OTP code has expired.")
    else:
        if is_otp_expired(user["created_at"]):
            raise OtpExpiredException(message="OTP code has expired.")

    if hash_otp_code(verify_data["otp"]) != user.get("verification_token"):
        raise InvalidOtpException(message="Invalid OTP code.")

    Transactions.mark_user_verified(
        user_id=user["id"],
        db=db,
        verified_time=datetime.now(timezone.utc).isoformat(),
    )
    redis_client = get_redis_client()
    redis_client.delete(f"otp:resend:count:{user['id']}")
    redis_client.delete(f"otp:resend:cooldown:{user['id']}")

    return {
        "status": "success",
        "message": "Account verified successfully.",
    }
