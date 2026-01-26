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