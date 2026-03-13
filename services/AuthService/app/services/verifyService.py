# from datetime import datetime, timezone

# from ..db.transactions import Transactions
# from app.utils.rate_limiter import get_redis_client
from ..exceptions.registerExceptions import (
    InvalidOtpException,
    OtpExpiredException,
    UserAlreadyVerifiedException,
    UserNotFoundException,
    otpNotSendFromSystem,
    userNotAllowedToModified,
    optSmsNotAllowedToModified
)
from ..util import hash_otp_code, get_current_local_time, back_to_localtime, current_time
from ..db.usesrs import userTransactions
# from ..db.sms_sender import smsSenderTransactions
from ..db.otp_attempts import otpAttenptsTransactions
from ..util import smsPurposeEnum, hash_otp_code


def verify_service(verify_data, db):
    """
    vefiry user by sms OTP
    
    :param verify_data: data that provide by user ( mobile number, otp )
    :type verify_data: dict
    :param db: database connection
    :type db: Client
    """
    # check the user are avilable by provided mobile number
    user = userTransactions.get_usser_detials_by_mobilenumer(verify_data["mobile_number"], db=db)
    if user["status"] == False:
        raise UserNotFoundException(message="User not found.")

    # check the user is verified or not
    if user["data"][0]['verified'] == True:
        raise UserAlreadyVerifiedException(message="User already verified.")

    # check the latest verification code expiry time
    latest_otp = otpAttenptsTransactions.get_latest_otp_attempt(user_id=user["data"][0]["id"], purpose=smsPurposeEnum.verification.value, db=db)
    if latest_otp == None:
        raise otpNotSendFromSystem(message="not ditect any send OTP from the system")
    elif back_to_localtime(latest_otp['expire_at']) < current_time():
        raise OtpExpiredException(message="OTP code has expired.")
    
    # check provide otp is match with existing code
    elif hash_otp_code(verify_data["otp"]) != latest_otp['otp_hash']:
        raise InvalidOtpException(message="Invalid OTP code.")

    # update user table
    update_user = userTransactions.update_user_by_mobile_number({'verified' : True, 'verifired_time' : get_current_local_time(hours=5, minutes=30)}, verify_data['mobile_number'], db)
    if update_user == False:
        raise userNotAllowedToModified(message='user table not allowed to modify')

    # update otp_sms table
    update_otp_sms = otpAttenptsTransactions.update_otp_sms({"used_status" : True, "used_time" : get_current_local_time(hours=5, minutes=30)}, latest_otp['id'], db)
    if update_otp_sms == False:
        raise optSmsNotAllowedToModified(message="OTP_SMS not allowed to modify")
    
    # final output
    return {
        "status": "success",
        "message": "Account verified successfully.",
    }