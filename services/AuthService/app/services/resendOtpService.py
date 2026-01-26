from ..db.usesrs import userTransactions
from app.utils.rate_limiter import get_redis_client
from ..exceptions.registerExceptions import (
    ResendOtpCooldownException,
    UserAlreadyVerifiedException,
    UserNotFoundException,
    databaseUpdateFaildException
)
from ..util import generate_otp_code, hash_otp_code, send_otp_sms, check_cooldown_key, log_sms_sender_payload, create_otp_attempt_payload, set_cooldown_key
from ..db.sms_sender import smsSenderTransactions
from ..db.otp_attempts import otpAttenptsTransactions

RESEND_LIMIT = 3
RESEND_WINDOW_SECONDS = 600
RESEND_COOLDOWN_SECONDS = 60


def resend_otp_service(resend_data, db):
    """
    resend otp service for the account verification
    
    :param resend_data: data
    :param db: database connection
    """
    # create redis client
    redis_client = get_redis_client()

    # check mobile number available on user database
    user_availability = userTransactions.get_usser_detials_by_mobilenumer(number=resend_data["mobile_number"], db=db)
    print(user_availability)
    if user_availability['status'] == False:
        return UserNotFoundException(message="User not found.")

    # check user verified or not
    if user_availability['data'][0]['verified'] == True:
        return UserAlreadyVerifiedException(message="User already verified.")

    # check the otp send rate limits
    check_cooldownkey = check_cooldown_key(redis_client=redis_client, id=user_availability['data'][0]['id'])
    if check_cooldownkey == True:
        return ResendOtpCooldownException(message="user previose OTP code. it's still not expired.")

    # generate new otp code
    otp_code = generate_otp_code()    

    # store in cache database
    set_cache = set_cooldown_key(resend_cooldown_seconds=RESEND_COOLDOWN_SECONDS, redis_client=redis_client, id=user_availability['data'][0]['id'])
    if set_cache == False:
        return databaseUpdateFaildException(message="redis db not updated")

    # send otp to the mobile number 
    send_id = send_otp_sms(otp_code=otp_code, recipient=resend_data["mobile_number"])

    # store the otp attempt
    store_otp = otpAttenptsTransactions.create_otp_attempt(db=db, payload=create_otp_attempt_payload(otp_code=hash_otp_code(otp_code), user_id=user_availability['data'][0]['id']))
    if store_otp['status'] == False:
        raise databaseUpdateFaildException("Failed to store OTP attempt. please try again later.")

    # store in sms logs
    store_sms_log = smsSenderTransactions.log_sms_sender(db=db, payload=log_sms_sender_payload(perpose='verification', sms_id=send_id, user_id=user_availability['data'][0]['id']))
    if store_sms_log['status'] == False:
        return databaseUpdateFaildException("Failed to log SMS sender. please try again later.")

    # return result
    return {
        "status": "success",
        "message": "OTP resent successfully.",
    }