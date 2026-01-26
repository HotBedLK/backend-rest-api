from ..db.usesrs import userTransactions
from ..db.sms_sender import smsSenderTransactions
from ..db.otp_attempts import otpAttenptsTransactions
from ..util import generate_otp_code,  send_otp_sms, create_otp_attempt_payload, log_sms_sender_payload, set_cooldown_key
from fastapi.responses import JSONResponse
from ..exceptions.registerExceptions import databaseUpdateFaildException, UserNotFoundException
from app.utils.rate_limiter import get_redis_client

RESEND_LIMIT = 3
RESEND_WINDOW_SECONDS = 600
RESEND_COOLDOWN_SECONDS = 60

def checkMobileNumber(data, db):
    """
    check user's mobile number in the database or not, and send verification code
    
    :param data: mobile number
    :param db: database connection
    """
    # create redis client
    redis_client = get_redis_client()

    # check the mobile number on db
    checkDb = userTransactions.get_usser_detials_by_mobilenumer(data.mobile_number, db)
    if checkDb['status'] == False:
        return UserNotFoundException(message="there is no user under this mobile number")
    
    # send the OPT to the mobile number
    otp_code = generate_otp_code()

    # send code to mobile number
    send_id = send_otp_sms(recipient=checkDb['data'][0]['mobile_number'], otp_code=otp_code)

    # store in otp attempt table
    store_otp_attempt = otpAttenptsTransactions.create_otp_attempt(payload=create_otp_attempt_payload(user_id=checkDb['data'][0]['id'], otp_code=otp_code), db=db)
    if store_otp_attempt['status'] == False:
        return databaseUpdateFaildException(message="Fail to store otp attempt in db")

    # store in sms logs
    store_sms_log = smsSenderTransactions.log_sms_sender(db=db, payload=log_sms_sender_payload(perpose='verification', sms_id=send_id, user_id=checkDb['data'][0]['id']))
    if store_sms_log['status'] == False:
        return databaseUpdateFaildException("Failed to log SMS sender. please try again later.")

    # store in cache database
    set_cache = set_cooldown_key(resend_cooldown_seconds=RESEND_COOLDOWN_SECONDS, redis_client=redis_client, id=checkDb['data'][0]['id'])
    if set_cache == False:
        return databaseUpdateFaildException(message="redis db not updated")

    # send success message
    return JSONResponse(status_code=200, content={
                "status": "success",
                "message": "OTP sent to mobile number."
            }
        )