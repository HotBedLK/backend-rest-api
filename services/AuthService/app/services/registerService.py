from ..db.transactions import Transactions
from ..exceptions.registerExceptions import (
    UserEmailAlreadyExistsException,
    UserNumberAlreadyExistsException,
)
from datetime import datetime, timedelta, timezone

from ..util import build_user_payload, generate_otp_code, hash_otp_code, send_otp_sms

def registerService(registerData,db):
    """
    Docstring for registerService
    Register a user using user details and send sms otp messages to phone number
    """

    #check user existance by email address
    exist_userByEmail = Transactions.check_user_by_email(email=registerData["email"],db=db)
    if exist_userByEmail:
        raise UserEmailAlreadyExistsException(message="This email is already exists in the system. try to login with that email.")
    
    #check user existance by phone number
    exist_userByNumber = Transactions.check_user_by_phonenumber(number=registerData["mobile_number"],db=db)
    if exist_userByNumber:
        raise UserNumberAlreadyExistsException(message="This phone number is already exists in the system. try to login with that number")

    otp_code = generate_otp_code()
    payload = build_user_payload(registerData, otp_code)
    created_users = Transactions.create_user(payload=payload, db=db)
    user_id = created_users[0]["id"] if created_users else None

    if user_id:
        sent_at = datetime.now(timezone.utc)
        expires_at = sent_at + timedelta(minutes=10)
        Transactions.create_otp_attempt(
            payload={
                "user_id": user_id,
                "otp_hash": hash_otp_code(otp_code),
                "sent_at": sent_at.isoformat(),
                "expires_at": expires_at.isoformat(),
                "send_count": 1,
                "status": "sent",
            },
            db=db,
        )
    send_otp_sms(recipient=registerData["mobile_number"], otp_code=otp_code)
    return {
        "status": "success",
        "message": "User created. Verification code sent.",
    }
