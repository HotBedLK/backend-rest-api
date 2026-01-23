from fastapi.responses import JSONResponse
from ..db.transactions import Transactions
from ..exceptions.registerExceptions import UserNotFoundException, userNotAllowedToModified, databaseUpdateFaildException
from app.services.jwt import encodePassword

def changePasswordService(data, db):
    # check the mobile number exists
    checkNumber = Transactions.get_usser_detials_by_mobilenumer(data.mobile_number, db)
    if checkNumber is False:
        return UserNotFoundException(message="Mobile number not found")
    
    # check the mobile number allow to change password
    if checkNumber['data'][0]['modify_account'] is False:
        return userNotAllowedToModified(message="User is not verified to change password")

    # update the password in the database
    updateUser = Transactions.update_user_details(checkNumber['data'][0]['id'], {"password": encodePassword(data.password)}, db)
    if updateUser is False:
        return databaseUpdateFaildException(message="Failed to update the password")

    # send success message
    return JSONResponse(status_code=200, content={"message": "Password changed successfully"})