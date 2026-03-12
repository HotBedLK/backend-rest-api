from ..db.usesrs import userTransactions
# from app.utils.rate_limiter import get_redis_client
from ..exceptions.registerExceptions import (
    ResendOtpCooldownException,
    UserAlreadyVerifiedException,
    UserNotFoundException,
    databaseUpdateFaildException
)
from ..util import generate_otp_code, hash_otp_code, send_otp_sms, create_otp_sms_payload,
from ..db.otp_attempts import otpAttenptsTransactions

RESEND_LIMIT = 3
RESEND_WINDOW_minutes = 10


def resend_otp_service(resend_data, db):
    """
    resend otp service for the account verification
    
    :param resend_data: data
    :param db: database connection
    """

    # check mobile number available on user database
    user_availability = userTransactions.get_usser_detials_by_mobilenumer(number=resend_data["mobile_number"], db=db)
    if user_availability['status'] == False:
        return UserNotFoundException(message="User not found.")

    # check user verified or not
    if user_availability['data'][0]['verified'] == True:
        return UserAlreadyVerifiedException(message="User already verified.")

    # check the otp send rate limits - this must rewrite with database interactions
    rate_limit = otpAttenptsTransactions.check_verification_otp_ratelimit(id=user_availability["data"][0]["id"], db=db, resend_limit=RESEND_LIMIT, resend_window_minutes=RESEND_WINDOW_minutes)
    if rate_limit == True:
        return ResendOtpCooldownException(message="user previose OTP code. it's still not expired.")
 
    # generate new otp code
    otp_code = generate_otp_code()    
 
    # send otp to the mobile number 
    send_id = send_otp_sms(otp_code=otp_code, recipient=resend_data["mobile_number"])

    # store the otp_sms table
    store_otp = otpAttenptsTransactions.create_otp_sms(db=db, payload=create_otp_sms_payload(otp_code=hash_otp_code(otp_code), user_id=user_availability["data"][0]["id"], sms_id=send_id))
    if store_otp['status'] == False:
        raise databaseUpdateFaildException("Failed to store OTP attempt. please try again later.")

    # return result
    return {
        "status": "success",
        "message": "OTP resent successfully.",
    }