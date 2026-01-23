from supabase import Client
from postgrest.exceptions import APIError
from ..exceptions.registerExceptions import SupabaseApiFailException

class Transactions:
    #check user existance via email address
    @staticmethod
    def check_user_by_email(email, db: Client):
        try:
            user = db.table("Users").select("email").eq('email',email).execute()
            if len(user.data) == 0:
                return False
            return True
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc
        

    #check user existance via email address
    @staticmethod
    def check_user_by_phonenumber(number, db: Client):
        try:
            user = db.table("Users").select("mobile_number").eq('mobile_number',number).execute()
            if len(user.data) == 0:
                return False
            return True
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc

    @staticmethod
    def create_user(payload: dict, db: Client):
        try:
            response = db.table("Users").insert(payload).execute()
            return response.data
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc

    @staticmethod
    def get_user_for_verification_by_email(email: str, db: Client):
        try:
            response = (
                db.table("Users")
                .select("id,email,mobile_number,verification_token,verified,created_at")
                .eq("email", email)
                .execute()
            )
            if not response.data:
                return None
            return response.data[0]
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc

    @staticmethod
    def get_user_for_verification_by_mobile(number: str, db: Client):
        try:
            response = (
                db.table("Users")
                .select("id,email,mobile_number,verification_token,verified,created_at")
                .eq("mobile_number", number)
                .execute()
            )
            if not response.data:
                return None
            return response.data[0]
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc

    @staticmethod
    def mark_user_verified(user_id: str, db: Client, verified_time: str):
        try:
            response = (
                db.table("Users")
                .update({"verified": True, "verifired_time": verified_time})
                .eq("id", user_id)
                .execute()
            )
            return response.data
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc

    @staticmethod
    def update_verification_token(user_id: str, token_hash: str, db: Client):
        try:
            response = (
                db.table("Users")
                .update({"verification_token": token_hash, "verified": False})
                .eq("id", user_id)
                .execute()
            )
            return response.data
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc

    @staticmethod
    def create_otp_attempt(payload: dict, db: Client):
        try:
            response = db.table("otp_attempts").insert(payload).execute()
            return response.data
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc

    @staticmethod
    def get_latest_otp_attempt(user_id: str, db: Client):
        try:
            response = (
                db.table("otp_attempts")
                .select("id,otp_hash,sent_at,expires_at,send_count,status")
                .eq("user_id", user_id)
                .order("sent_at", desc=True)
                .limit(1)
                .execute()
            )
            if not response.data:
                return None
            return response.data[0]
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc
        
    @staticmethod
    def get_usser_detials_by_mobilenumer(mobile_number:str, db:Client):
        try:
            user = (
                db.table("Users")
                .select("*")
                .eq("mobile_number", mobile_number)
                .execute()
            )
            if len(user.data) != 0:
                return {
                    'data' : user.data,
                    'status' : True
                }
            else:
                return {
                    'data' : user.data,
                    'status' : False     
                }
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc

    @staticmethod
    def get_newest_otp_by_userid(user_id:str, db:Client):
        try:
            otp_record = (
                db.table("otp_attempts")
                .select("*")
                .eq("user_id", user_id)
                .order("sent_at", desc=True)
                .limit(1)
                .execute()
            )
            if len(otp_record.data) != 0:
                return {
                    'data' : otp_record.data,
                    'status' : True
                }
            else:
                return {
                    'data' : otp_record.data,
                    'status' : False     
                }
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc

    @staticmethod
    def update_otp_attempt_status(otp_id: str, status: str, db: Client):
        try:
            response = (
                db.table("otp_attempts")
                .update({"status": status})
                .eq("id", otp_id)
                .execute()
            )
            if len(response.data) == 0:
                return False
            else:
                return True
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc

    @staticmethod
    def change_modify_account_status(id : str, status : bool, db : Client):
        try:
            response = (
                db.table("Users")
                .update({"modify_account": status})
                .eq("id", id)
                .execute()
            )
            if len(response.data) == 0:
                return False
            else:
                return True
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc

    @staticmethod
    def update_user_details(user_id: str, update_data: dict, db: Client):
        try:
            response = (
                db.table("Users")
                .update(update_data)
                .eq("id", user_id)
                .execute()
            )
            if len(response.data) == 0:
                return False
            else:
                return True
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc