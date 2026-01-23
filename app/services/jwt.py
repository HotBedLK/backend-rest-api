from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from passlib.hash import pbkdf2_sha256
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends
from typing import Annotated
from fastapi import HTTPException, status
from datetime import datetime, timedelta


load_dotenv()
security = HTTPBearer()

jwt_key = os.getenv('JWT_SECRET_KEY')
jwt_algorithm = os.getenv('JWT_ALGORITHM')
jwt_refresh_key = os.getenv('JWT_REFRESH_KEY')

def encodeToken(mobileNumber, role):
    """
    Generate JWT token using passed parameters
    
    :param email: user email address
    :param role: user role in the system [lister, viwer, admin]
    """
    try:
        token = jwt.encode({'mobileNumber': mobileNumber,
                        'role': role}, jwt_key, algorithm=jwt_algorithm)
        return token
    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail="Error in token generation")

def encodeRefreshTocken(userId : str):
    """
    create refresh token for the user
    
    :param userId: id of the user
    """
    # set all needed payload for refresh token
    ist = datetime.now().timestamp()
    jti = f"{userId}-{ist}"
    exp = ist + timedelta(days=30).total_seconds()
    
    # try to create a refresh token
    try:
        token = jwt.encode(
            {'userId': userId,
             'ist' : ist,
             'jti' : jti,
             'exp'  : exp,
            'type': 'refresh' }, jwt_refresh_key, algorithm=jwt_algorithm)
        return token
    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail="Error in token generation")


def decodeToken(token):
    """
    decode JWT token and return the data
    
    :param token: JWT token that pass by user
    """
    try:
        data = jwt.decode(token, jwt_key, algorithms=[jwt_algorithm])
        return data
    except JWTError:
        return False

def decodeRefreshToken(token):
    """
    decode refresh JWT token and return the data
    
    :param token: refresh JWT token that pass by user
    """
    
    try:
        data = jwt.decode(token, jwt_refresh_key, algorithms=[jwt_algorithm])
        return data
    except JWTError:
        return False

def encodePassword(plainPassword):
    """
    encode plain password to encripted password that pass by user
    
    :param plainPassword: user plain password
    """
    try:
        encriptPassword = pbkdf2_sha256.hash(plainPassword)
        return encriptPassword
    except Exception as e:
        return 'error in password encryption'

# decode password
def decodePasword(palinPassword, encriptPassword):
    """
    decode encrypted password and compare with plain passwords
    
    :param palinPassword: user plain password
    :param encriptPassword: user encrypted password that get from db
    """
    try:
        decriptedPassword = pbkdf2_sha256.verify(palinPassword, encriptPassword)
        return decriptedPassword
    except Exception as e:
        return 'error in password decryption'
    
# deal with barer token
def authVerification(details: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    """
    verify the barer token and decode the token data
    
    :param details: HTTP authorization credentials
    """
    return decodeToken(details.credentials)