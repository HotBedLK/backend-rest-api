from fastapi.responses import JSONResponse
from ..db.usesrs import userTransactions
from ..exceptions.registerExceptions import UserNotFoundException, userNotAllowedToModified, databaseUpdateFaildException
from app.services.jwt import encodePassword
from ..util import user_update_payload

def changePasswordService(data, db):
    # check the mobile number exists - this should be modify
    checkNumber = userTransactions.get_usser_detials_by_mobilenumer(number=data.mobile_number, db=db)
    # print(checkNumber)
    if checkNumber is False:
        raise UserNotFoundException(message="Mobile number not found")

    # check the mobile number allow to change password
    if checkNumber['data'][0]['modify_account'] is False:
        raise userNotAllowedToModified(message="User is not verified to change password")
    
    # upadate related field on 'User' table
    updateUser = userTransactions.update_user_by_mobile_number(payload=user_update_payload(password=data.password, modify_account=False,), mobile_number=data.mobile_number, db=db)
    if updateUser is False:
        return databaseUpdateFaildException(message="Failed to update the password")

    # send success message
    return JSONResponse(status_code=200, content={
        "message": "Password changed successfully"
        })