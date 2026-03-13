# from ..db.transactions import Transactions 
from ..util import is_otp_expired, compair_otp_codes
from fastapi.responses import JSONResponse
from ..exceptions.registerExceptions import UserNotFoundException, vefiricationCodeNotFoundException, OtpExpiredException, InvalidOtpException, databaseUpdateFaildException
from ..util import smsPurposeEnum, user_update_payload, update_otp_sms_table_payload
from ..db.usesrs import userTransactions
# from ..db.sms_sender import smsSenderTransactions
from ..db.otp_attempts import otpAttenptsTransactions

def verifyMobileNumberService(data, db):
    """
    verify mobile number ownership / hold in hand using OTP
    param data : all data provided by user
    param db : database connection
    """

    # Check if the mobile number exists in the database.
    numberAvailability = userTransactions.get_usser_detials_by_mobilenumer(data.mobile_number, db)
    if numberAvailability['status'] == False:
        return UserNotFoundException("user not found from this email")
    
    # get last record for the opt send using user id
    # lastVeficationCode = smsSenderTransactions.get_latest_otp_attempt(user_id=numberAvailability['data'][0]['id'], db=db, purpose=data.purpose.value)
    lastVeficationCode = otpAttenptsTransactions.get_latest_otp_attempt(user_id=numberAvailability['data'][0]['id'], db=db, purpose=data.purpose.value)
    if lastVeficationCode == None:
        return vefiricationCodeNotFoundException("no otp found under this user")
    
    # check otp code expire or not
    codeExpire = is_otp_expired(lastVeficationCode["expire_at"])
    if codeExpire:
        return OtpExpiredException("the otp code is expired, please request a new one")
    
    # check the otp code validity
    otpValied = compair_otp_codes(data.otp, lastVeficationCode['otp_hash'])
    if not otpValied:
        return InvalidOtpException("the provided otp code is invalid")
    
    # update the 'otp-attempts' table
    updateOtpTable = otpAttenptsTransactions.update_otp_sms(payload=update_otp_sms_table_payload(status=True), id=lastVeficationCode['id'], db=db)
    if updateOtpTable == False:
        return databaseUpdateFaildException("failed to update otp attempt status")
    
    # this is for password reset
    if data.purpose == smsPurposeEnum.passwordreset.value:
        # updath the 'User' table's modify_account field
        upadateUserTable = userTransactions.update_user_by_mobile_number(payload=user_update_payload(modify_account=True), mobile_number=data.mobile_number, db=db)
        if upadateUserTable == False:
            return databaseUpdateFaildException("failed to update user verified status")

    # this is for account verification
    elif data.purpose == smsPurposeEnum.verification.value:
        # updath the 'User' table's verified field
        upadateUserTable = userTransactions.update_user_by_mobile_number(payload=user_update_payload(modify_account=True, verified=True), mobile_number=data.mobile_number, db=db)
        if upadateUserTable == False:
            return databaseUpdateFaildException("failed to update user verified status")
    
    # send success message
    return JSONResponse(status_code=200, content={
                "status": "success",
                "message": "mobile number verified."
            }
        )