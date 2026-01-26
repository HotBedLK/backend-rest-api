from ..db.usesrs import userTransactions
from ..db.sms_sender import smsSenderTransactions
from ..db.otp_attempts import otpAttenptsTransactions
from ..exceptions.registerExceptions import (
    UserNumberAlreadyExistsException,
    UserNotFoundException,
    databaseUpdateFaildException
)
from ..util import create_otp_attempt_payload, log_sms_sender_payload
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
    payload = build_user_payload(registerData, otp_code)
    
    # create new user
    created_users = userTransactions.create_user(payload=payload, db=db)
    if created_users['status'] == False:
        raise UserNotFoundException("User creation failed. please try again later.")

    # send opt to the mobile
    send_otp_id = send_otp_sms(recipient=registerData["mobile_number"], otp_code=otp_code)
    
    # store in otp attempts table
    store_otp_attempt = otpAttenptsTransactions.create_otp_attempt(create_otp_attempt_payload(user_id=created_users['data'][0]['id'], otp_code=otp_code), db=db)
    if store_otp_attempt['status'] == False:
        raise databaseUpdateFaildException("Failed to store OTP attempt. please try again later.")

    # store in sms logs table
    sms_logs = smsSenderTransactions.log_sms_sender(log_sms_sender_payload(user_id=created_users['data'][0]['id'], perpose="registration_otp", sms_id=send_otp_id), db=db)
    if sms_logs['status'] == False:
        raise databaseUpdateFaildException("Failed to log SMS sender. please try again later.")

    return {
        "status": "success",
        "message": "User created. Verification code sent.",
    }
