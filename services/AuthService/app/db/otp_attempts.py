from supabase import Client
from postgrest.exceptions import APIError
from ..exceptions.registerExceptions import SupabaseApiFailException
from ..util import get_previose_local_time

class otpAttenptsTransactions:

    @staticmethod
    def create_otp_sms(payload: dict, db: Client):
        """
        purpose : add data to the otp_sms table to recore all send sms regarding authontication sms sending

        :param payload : all data that want to populate table
        :param db : database client connection
        """
        try:
            response = db.table("otp_sms").insert(payload).execute()
            if len(response.data) == 0:
                return {
                    'status' : False,
                    'data' : response.data
                }
            else:
                return {
                    'status' : True,
                    'data' : response.data
                }
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc
        
    @staticmethod
    def update_otp_sms(payload: dict, id:str, db: Client):
        """
        purpose : update otp_sms table

        :param payload : updated data set
        :param id : user_id
        :param db : database client connection
        """
        try:
            response = db.table("otp_sms").update(payload).eq('id', id).execute()
            if len(response.data) == 0:
                return False
            else:
                return True
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc
        
    @staticmethod
    def check_verification_otp_ratelimit(id:str, db: Client, resend_limit = 3, resend_window_minutes = 10):
        """
        purpose : check how many account verification otp send withign given time periode

        :param id : user_id
        :param db : database client connection
        """
        try:
            response = db.table("otp_sms").select('created_at').eq('user_id', id).lt("created_at", get_previose_local_time(minutes=resend_window_minutes)).order("created_at", desc=True).limit(3).execute()
            if len(response.data) < resend_limit:
                return False
            else:
                return True
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc