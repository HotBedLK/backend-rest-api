from supabase import Client
from postgrest.exceptions import APIError
from ..exceptions.registerExceptions import SupabaseApiFailException

class smsSenderTransactions:

    @staticmethod
    def log_sms_sender(payload: dict, db: Client):
        """
        log sms sender details
        
        :param payload: sms sender data
        :type payload: dict
        :param db: database connection
        :type db: Client
        """
        try:
            # store data on database
            response = db.table("sms_sender").insert(payload).execute()
            
            # return response.data
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
            # raise exceptios
            raise SupabaseApiFailException(message=str(exc)) from exc
        
    @staticmethod
    def get_latest_otp_attempt(user_id: str, db: Client):
        """
        purpose : get latest otp attemp base on user's id
        
        :param user_id: UUID of the user 
        :type payload: dict
        :param db: database connection
        :type db: Client
        """
        try:
            response = (
                db.table("otp_sms")
                .select("id,otp_hash,expire_at, used_status, used_time")
                .eq("user_id", user_id)
                .eq("purpose", "verification")
                .order("send_at", desc=True)
                .limit(1)
                .execute()
            )
            if not response.data:
                return None
            return response.data[0]
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc