from ..db.usesrs import userTransactions
from ..exceptions.registerExceptions import credencialsNotMatchedException
from app.services import jwt
from fastapi.responses import JSONResponse

def loginService(loginData:dict,db):
    """
    check user allowed to services or not using users mobile number and password
    
    :param loginData: mobile_number and passwrod
    :type loginData: dict
    :param db: database connection
    """    
    # check the mobile number is exist or not
    user_exists = userTransactions.get_usser_detials_by_mobilenumer(number=loginData["mobile_number"],db=db)
    if user_exists['status'] == False:
        raise credencialsNotMatchedException("credencials not matched. please check and try again.")

    # # check the password is correct or not (compaire plain password with hashed password)
    data = jwt.decodePasword(palinPassword=loginData["password"], encriptPassword=user_exists["data"][0]["password"])
    if data == False:
        raise credencialsNotMatchedException("credencials not matched. please check and try again.")

    # issue refresh key
    refreshKey = jwt.encodeRefreshTocken(user_exists["data"][0]["id"])

    # issue the JWT token
    jwtToken = jwt.encodeToken(mobileNumber=user_exists["data"][0]["mobile_number"], role=user_exists["data"][0]["user_role"])
    
    # return the token
    return JSONResponse(status_code=200, content={
        "status": "success",
        "token": jwtToken,
        "refresh_token" : refreshKey
    })