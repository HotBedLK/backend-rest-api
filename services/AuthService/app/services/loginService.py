from ..db.transactions import Transactions
from ..exceptions.registerExceptions import credencialsNotMatchedException
from app.services import jwt
from fastapi.responses import JSONResponse

def loginService(loginData:dict,db):
    pass
    # check the mobile number is exist or not
    user_exists = Transactions.get_usser_detials_by_mobilenumer(mobile_number=loginData["mobile_number"],db=db)
    if user_exists['status'] == False:
        raise credencialsNotMatchedException("credencials not matched. please check and try again.")
    print(user_exists)

    # # check the password is correct or not (compaire plain password with hashed password)
    print(loginData["password"], user_exists["data"][0]["password"])
    data = jwt.decodePasword(palinPassword=loginData["password"], encriptPassword=user_exists["data"][0]["password"])
    if data == False:
        raise credencialsNotMatchedException("credencials not matched. please check and try again.")

    # issue refresh key
    refreshKey = jwt.encodeRefreshTocken(user_exists["data"][0]["id"])

    # issue the JWT token
    createToken = jwt.encodeToken(mobileNumber=user_exists["data"][0]["mobile_number"], role=user_exists["data"][0]["user_role"])
    print(f'this is for token {createToken}')
    
    # return the token
    return JSONResponse(status_code=200, content={
        "status": "success",
        "token": createToken,
        "refresh_token" : refreshKey
    })