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
        
    @staticmethod
    def get_usser_detials_by_mobilenumer(number: str, db: Client):
        """
        search mobile number in 'user' table. if so give id, verified fields
        
        :param number: Description
        :type number: str
        :param db: Description
        :type db: Client
        """
        try:
            response = (
                db.table("Users")
                .select("id,verified,password,mobile_number,user_role")
                .eq("mobile_number", number)
                .execute()
            )
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
            # return response.data[0]
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc
        
    @staticmethod
    def update_user_by_mobile_number(payload:dict, mobile_number:str, db:Client):
        """
        update any user field reffering user's mobile number
        
        :param payload: all the filed want to update
        :type number: dict
        :param mobile_number: user's mobile number
        :type db: str
        :param db: Description
        :type db: Client
        """
        try:
            user = db.table('Users').update(payload).eq('mobile_number', mobile_number).execute()
             # return boolean value
            if len(user.data) == 0:
                return False
            else:
                return True
        except APIError as exc:
            # raise exceptios
            raise SupabaseApiFailException(message=str(exc)) from exc