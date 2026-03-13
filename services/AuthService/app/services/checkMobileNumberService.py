from ..db.usesrs import userTransactions
from ..db.sms_sender import smsSenderTransactions
from ..db.otp_attempts import otpAttenptsTransactions
from ..util import generate_otp_code,  send_otp_sms, create_otp_sms_payload, log_sms_sender_payload, set_cooldown_key, user_update_payload
from fastapi.responses import JSONResponse
from ..exceptions.registerExceptions import databaseUpdateFaildException, UserNotFoundException, verificationCodeAlredySendException, userNotAllowedToModified
from ..util import userRoleEnum, smsPurposeEnum

RESEND_LIMIT = 3
RESEND_WINDOW_MINUTES = 10
# RESEND_COOLDOWN_MINUTES = 10

def checkMobileNumber(data, db):
    """
    check user's mobile number in the database or not, and send verification code
    
    :param data: mobile number
    :param db: database connection
    """

    # check the mobile number on db
    checkDb = userTransactions.get_usser_detials_by_mobilenumer(data.mobile_number, db)
    if checkDb['status'] == False:
        return UserNotFoundException(message="there is no user under this mobile number")
    
    # generate OTP code
    otp_code = generate_otp_code()

    # check how many loging attempts withing given time period
    rate_limit = otpAttenptsTransactions.check_login_otp_ratelimit(id=checkDb['data'][0]['id'], db=db, resend_limit=RESEND_LIMIT, resend_window_minutes=RESEND_WINDOW_MINUTES)
    if rate_limit == True:
        raise verificationCodeAlredySendException(message="use alredy sent verification code or wait for while")

    # send code to mobile number
    send_id = send_otp_sms(recipient=checkDb['data'][0]['mobile_number'], otp_code=otp_code)

    # store in otp_sms table
    store_otp_attempt = otpAttenptsTransactions.create_otp_sms(payload=create_otp_sms_payload(purpose=smsPurposeEnum.passwordreset.value, user_id=checkDb['data'][0]['id'], otp_code=otp_code, sms_id=send_id), db=db)
    if store_otp_attempt['status'] == False:
        raise databaseUpdateFaildException(message="Fail to store otp attempt in db")

    # allowed user table modify
    modify_user = userTransactions.update_user_by_mobile_number(payload=user_update_payload(mobile_number=data.mobile_number , modify_account=True), mobile_number=data.mobile_number, db=db)
    if modify_user == False:
        raise userNotAllowedToModified(message="user not allowed to modify account")

    # send success message
    return JSONResponse(status_code=200, content={
                "status": "success",
                "message": "OTP sent to mobile number."
            }
        )