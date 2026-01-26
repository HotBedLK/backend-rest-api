from supabase import Client
from postgrest.exceptions import APIError
from ..exceptions.registerExceptions import SupabaseApiFailException

class otpAttenptsTransactions:

    @staticmethod
    def create_otp_attempt(payload: dict, db: Client):
        try:
            response = db.table("otp_attempts").insert(payload).execute()
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