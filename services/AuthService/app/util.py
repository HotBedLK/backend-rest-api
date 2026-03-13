import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from enum import Enum

from dateutil import parser

import httpx
from decouple import config, UndefinedValueError

from .exceptions.registerExceptions import (
    InvalidMobileNumberException,
    SmsGatewayConfigException,
    SmsGatewayException,
    payloadCreationException
)


def generate_otp_code() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"


def hash_otp_code(otp_code: str) -> str:
    return hashlib.sha256(otp_code.encode("utf-8")).hexdigest()


def is_otp_expired(created_at: str, ttl_minutes: int = 10) -> bool:
    created_time = parser.isoparse(created_at)
    if created_time.tzinfo is None:
        created_time = created_time.replace(tzinfo=timezone.utc)
    return datetime.now(timezone.utc) > created_time + timedelta(minutes=ttl_minutes)


def is_timestamp_expired(expires_at: str) -> bool:
    expiry_time = parser.isoparse(expires_at)
    if expiry_time.tzinfo is None:
        expiry_time = expiry_time.replace(tzinfo=timezone.utc)
    return datetime.now(timezone.utc) > expiry_time


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
    return f"pbkdf2_sha256$200000${salt.hex()}${derived.hex()}"


def build_user_payload(register_data: dict, otp) -> dict:
    return {
        "first_name": register_data["first_name"],
        "last_name": register_data["last_name"],
        "password": hash_password(register_data["password"]),
        "mobile_number": register_data["mobile_number"],
        "verified": False,
        "verifired_time": None,
        "premium": False,
        "user_role": userRoleEnum.viewer.value,
        'modify_account' : False,
        'created_at' : get_current_local_time(),
    }


def _get_sms_config() -> tuple[str, str]:
    try:
        return (
            config("TEXTLK_API_TOKEN"),
            config("TEXTLK_SENDER_ID"),
        )
    except UndefinedValueError as exc:
        raise SmsGatewayConfigException(
            message="Missing TEXTLK_API_TOKEN or TEXTLK_SENDER_ID environment variable."
        ) from exc


# this must transfer to the main app utils file
def send_otp_sms(recipient: str, otp_code: str):
    api_token, sender_id = _get_sms_config()
    normalized_recipient = normalize_mobile_number(recipient)
    
    # create payload and headers
    payload = {
        "recipient": normalized_recipient,
        "sender_id": sender_id,
        "type": "plain",
        "message": f"Your verification code is {otp_code}",
    }
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    try:
        # try to send sms
        response = httpx.post(
            "https://app.text.lk/api/v3/sms/send",
            json=payload,
            headers=headers,
            timeout=10.0,
        )
        data = response.json()
        print(data)
        return data['data']['uid']
    
    except httpx.HTTPError as exc:
        # raise and exceptions
        raise SmsGatewayException(message="Failed to reach SMS gateway.") from exc

    # if data.get("status") != "success":
    #     raise SmsGatewayException(
    #         message=data.get("message", "SMS gateway returned an error.")
    #     )


def normalize_mobile_number(number: str) -> str:
    cleaned = "".join(ch for ch in number if ch.isdigit())
    if cleaned.startswith("0") and len(cleaned) == 10:
        return f"94{cleaned[1:]}"
    if cleaned.startswith("94") and len(cleaned) == 11:
        return cleaned
    raise InvalidMobileNumberException(
        message="Mobile number must be 10 digits starting with 0 or 11 digits starting with 94."
    )

def compair_otp_codes(provided_otp: str, stored_hashed_otp: str) -> bool:
    return hash_otp_code(str(provided_otp)) == stored_hashed_otp


# *update registration, verification and otp_code resend endpoints as well
# changes 1 : add purpose
def create_otp_sms_payload(purpose ,user_id, otp_code, sms_id):
    """
    create a payload for otp attempts table

    :param user_id: id of the user
    :param otp_code: otp code
    """
    try:
        # sent_at = datetime.now(timezone.utc)
        # expires_at = sent_at + timedelta(minutes=10)
        payload = {
                "user_id": user_id,
                "otp_hash": hash_otp_code(otp_code),
                # "sent_at": sent_at.isoformat(),
                "send_at": get_current_local_time(),
                # "expires_at": expires_at.isoformat(),
                "expire_at": get_current_local_time(hours=3),
                "used_status": False,
                'created_at' : get_current_local_time(),
                'purpose' : purpose,
                'used_time' : None,
                'sms_id' : sms_id
            }
        print(payload)

        return payload 
    except Exception as exc:
        raise payloadCreationException("Failed to create OTP attempt payload.") from exc

def log_sms_sender_payload(user_id, perpose, sms_id):
    """
    create payload for the log sms sender
    
    :param user_id: id of the user
    :param perpose: perpose of send sms
    :param sms_id: sms_id get from sms gateway
    """
    try:
        return {
            'user_id' : user_id,
            'created_at' : datetime.now(timezone.utc).isoformat(),
            'perpose' : perpose,
            'sms_id' : sms_id,
        }
    except Exception as exc:
        raise payloadCreationException("Failed to create log sms sender payload.") from exc
    
def user_update_payload(modify_account:bool= None, verified:bool = None):
    """
    create payload for update user table
    
    :param user_id: id of the user
    :param perpose: perpose of send sms
    :param sms_id: sms_id get from sms gateway
    """
    payload = {
        # this is for common field for all updates happend on user table
        'updated_at': datetime.now(timezone.utc).isoformat()
    }

    # Dynamically add fields only if they are not None
    if modify_account is not None:
        payload['modify_account'] = modify_account
        
    if verified is not None:
        payload['verified'] = verified

    try:
        return payload
    except Exception as exc:
        raise payloadCreationException("Failed to create log sms sender payload.") from exc

def check_cooldown_key(redis_client, id):
    # recreate cooldown key
    cooldown_key = f"otp:resend:cooldown:{id}"
    
    # check cooldown key exist or not
    if redis_client.exists(cooldown_key):
        return True
    else:
        return False
    
def set_cooldown_key(redis_client, id, resend_cooldown_seconds):
    # creat a cooldown key
    cooldown_key = f"otp:resend:cooldown:{id}"
    
    # store in redis db
    store = redis_client.set(cooldown_key, 1, ex=resend_cooldown_seconds)
    
    # return the store status
    return store

class userRoleEnum(str, Enum):
    viewer = "viewer"
    editor = "lister"
    admin = "admin"

class smsPurposeEnum(str, Enum):
    verification  = 'verification'
    passwordreset = 'passwordreset'
    login = 'login'
    alert = 'alert'
    promotion = 'promotion'

def get_current_local_time(hours = 0, minutes = 0):
    # get sri japura timezone
    colombo_time = timezone(timedelta(hours=5, minutes=30))
    # add extra hours and minutes if needed
    new_time = datetime.now(colombo_time) + timedelta(hours=hours, minutes=minutes)
    return new_time.isoformat()

def get_previose_local_time(hours = 0, minutes = 0):
    # get sri japura timezone
    colombo_time = timezone(timedelta(hours=5, minutes=30))
    # add extra hours and minutes if needed
    new_time = datetime.now(colombo_time) - timedelta(hours=hours, minutes=minutes)
    return new_time.isoformat()

def current_time():
    # get sri japura timezone
    colombo_time = timezone(timedelta(hours=5, minutes=30))
    # add extra hours and minutes if needed
    new_time = datetime.now(colombo_time)
    return new_time

def back_to_localtime(provided_time):
    # convert string to datetime
    timed_format = datetime.fromisoformat(provided_time)
    # set as to Asia/colombo time some
    current_local_time = timed_format + timedelta(hours=5, minutes=30)
    return current_local_time