from ..db.usesrs import userTransactions
from ..db.otp_attempts import otpAttenptsTransactions
from ..exceptions.registerExceptions import (
    UserNumberAlreadyExistsException,
    UserNotFoundException,
    databaseUpdateFaildException
)
from ..util import create_otp_sms_payload, smsPurposeEnum
from ..util import build_user_payload, generate_otp_code, send_otp_sms

def registerService(registerData,db):
    """
    register new user in to the system
    
    :param registerData: all the data send from fronteend
    :param db: database connection
    """
   
    #check user existance by phone number
    exist_userByNumber = userTransactions.check_user_by_phonenumber(number=registerData["mobile_number"],db=db)
    if exist_userByNumber == True:
        raise UserNumberAlreadyExistsException(message="This phone number is already exists in the system. try to login with that number")

    # generate random otp
    otp_code = generate_otp_code()
    
    # create user payloadfrom 
    payload = build_user_payload(registerData)
    
    # send opt to the mobile
    send_otp_id = send_otp_sms(recipient=registerData["mobile_number"], otp_code=otp_code)
    
    # create new user
    created_users = userTransactions.create_user(payload=payload, db=db)
    if created_users['status'] == False:
        raise UserNotFoundException("User creation failed. please try again later.")
    
    # store in otp attempts table
    store_otp_attempt = otpAttenptsTransactions.create_otp_sms(create_otp_sms_payload(user_id=created_users['data'][0]['id'], otp_code=otp_code, sms_id = send_otp_id, purpose=smsPurposeEnum.verification.value), db=db)
    if store_otp_attempt['status'] == False:
        raise databaseUpdateFaildException("Failed to store OTP attempt. please try again later.")

    return {
        "status": "success",
        "message": "User created. Verification code sent.",
    }
