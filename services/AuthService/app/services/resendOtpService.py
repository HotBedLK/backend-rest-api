from datetime import datetime, timedelta, timezone

from app.utils.rate_limiter import get_redis_client
from ..db.transactions import Transactions
from ..exceptions.registerExceptions import (
    ResendOtpCooldownException,
    ResendOtpLimitException,
    UserAlreadyVerifiedException,
    UserNotFoundException,
)
from ..util import generate_otp_code, hash_otp_code, send_otp_sms

RESEND_LIMIT = 3
RESEND_WINDOW_SECONDS = 600
RESEND_COOLDOWN_SECONDS = 60


def resend_otp_service(resend_data, db):
    if resend_data.get("email"):
        user = Transactions.get_user_for_verification_by_email(
            email=resend_data["email"], db=db
        )
    else:
        user = Transactions.get_user_for_verification_by_mobile(
            number=resend_data["mobile_number"], db=db
        )

    if not user:
        raise UserNotFoundException(message="User not found.")

    if user.get("verified"):
        raise UserAlreadyVerifiedException(message="User already verified.")

    redis_client = get_redis_client()
    cooldown_key = f"otp:resend:cooldown:{user['id']}"
    if redis_client.exists(cooldown_key):
        raise ResendOtpCooldownException(
            message="Please wait before requesting another OTP."
        )

    count_key = f"otp:resend:count:{user['id']}"
    count = redis_client.incr(count_key)
    if count == 1:
        redis_client.expire(count_key, RESEND_WINDOW_SECONDS)

    if count > RESEND_LIMIT:
        raise ResendOtpLimitException(message="OTP resend limit reached.")

    redis_client.set(cooldown_key, "1", ex=RESEND_COOLDOWN_SECONDS)

    otp_code = generate_otp_code()
    token_hash = hash_otp_code(otp_code)
    Transactions.update_verification_token(user_id=user["id"], token_hash=token_hash, db=db)

    sent_at = datetime.now(timezone.utc)
    expires_at = sent_at + timedelta(minutes=10)
    Transactions.create_otp_attempt(
        payload={
            "user_id": user["id"],
            "otp_hash": token_hash,
            "sent_at": sent_at.isoformat(),
            "expires_at": expires_at.isoformat(),
            "send_count": count,
            "status": "sent",
        },
        db=db,
    )

    send_otp_sms(recipient=user["mobile_number"], otp_code=otp_code)

    return {
        "status": "success",
        "message": "OTP resent successfully.",
    }
