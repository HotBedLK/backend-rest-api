from supabase import Client
from postgrest.exceptions import APIError
from ..exceptions.registerExceptions import SupabaseApiFailException

class userTransactions:

    #check user existance via email address
    @staticmethod
    def check_user_by_phonenumber(number, db: Client):
        """
        check user by mobile number
        
        :param number: mobile number
        :type number: str
        :param db: database connection
        :type db: Client
        """
        try:
            # check user existance in database or not
            user = db.table("Users").select("mobile_number").eq('mobile_number',number).execute()
            
            # return boolean value
            if len(user.data) == 0:
                return False
            else:
                return True
        except APIError as exc:
            # raise exceptios
            raise SupabaseApiFailException(message=str(exc)) from exc
        
    @staticmethod
    def create_user(payload: dict, db: Client):
        """
        create new users
        
        :param payload: users data
        :type payload: dict
        :param db: database connection
        :type db: Client
        """
        try:
            # store data on database
            response = db.table("Users").insert(payload).execute()
            
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