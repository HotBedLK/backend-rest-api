from ..db.transactions import Transactions 
from ..util import generate_otp_code, hash_otp_code
from datetime import datetime, timezone, timedelta
from fastapi.responses import JSONResponse
from ..exceptions.registerExceptions import databaseUpdateFaildException


def checkMobileNumber(data, db):
    # check the mobile number on db
    checkDb = Transactions.get_usser_detials_by_mobilenumer(data.mobile_number, db)
    if checkDb['status'] == False:
        return {
            'status' : 'failed',
            'message' : 'mobile number not found'
        }
    
    # send the OPT to the mobile number
    otp_code = generate_otp_code()
    hashOpt = hash_otp_code(otp_code)

    # send code to mobile number
    # TODO: to be implemented. bellow is for temapry solution
    print(f"Sending OTP {otp_code} to mobile number {data.mobile_number}")

    # store in database
    sent_at = datetime.now(timezone.utc)
    expires_at = sent_at + timedelta(minutes=10)

    store = Transactions.create_otp_attempt(
        payload={
                "user_id": checkDb['data'][0]['id'],
                "otp_hash": hashOpt,
                "sent_at": sent_at.isoformat(),
                "expires_at": expires_at.isoformat(),
                "send_count": 1,
                "status": "sent",
            },
            db=db,
    )
    if len(store) == 0:
        # if return recode lenth is zero, return failed
        return  databaseUpdateFaildException(message="Failed to store OTP attempt in database.")

    # send success message
    return JSONResponse(status_code=200, content={
                "status": "success",
                "message": "OTP sent to mobile number."
            }
        )