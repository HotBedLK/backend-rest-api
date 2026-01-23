from ..db.transactions import Transactions 
from ..util import is_otp_expired, compair_otp_codes
from fastapi.responses import JSONResponse
from ..exceptions.registerExceptions import UserNotFoundException, vefiricationCodeNotFoundException, OtpExpiredException, InvalidOtpException, databaseUpdateFaildException


def verifyMobileNumberService(data, db):
    # Check if the mobile number exists in the database.
    numberAvailability = Transactions.get_usser_detials_by_mobilenumer(data.mobile_number, db)
    if numberAvailability['status'] == False:
        return UserNotFoundException("user not found from this email")

    # get last record for the opt send using user id
    lastVeficationCode = Transactions.get_newest_otp_by_userid(numberAvailability['data'][0]['id'], db)
    if lastVeficationCode['status'] == False:
        return vefiricationCodeNotFoundException("no otp found under this user")

    # check otp code expire or not
    codeExpire = is_otp_expired(lastVeficationCode['data'][0]['expires_at'])
    if codeExpire:
        return OtpExpiredException("the otp code is expired, please request a new one")

    # check the otp code validity
    otpValied = compair_otp_codes(data.otp, lastVeficationCode['data'][0]['otp_hash'])
    if not otpValied:
        return InvalidOtpException("the provided otp code is invalid")

    # update the 'otp-attempts' table
    updateOtpTable = Transactions.update_otp_attempt_status(lastVeficationCode['data'][0]['id'], 'used', db)
    if updateOtpTable == False:
        return databaseUpdateFaildException("failed to update otp attempt status")

    # updath the 'User' table
    upadateUserTable = Transactions.change_modify_account_status(numberAvailability['data'][0]['id'], True, db)
    if upadateUserTable == False:
        return databaseUpdateFaildException("failed to update user verified status")
    
    # send success message
    return JSONResponse(status_code=200, content={
                "status": "success",
                "message": "mobile number verified."
            }
        )