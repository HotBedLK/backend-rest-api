from supabase import Client
from services.SubscriptionService.app.ENUMS import PaymentStatus, SubscriptionStatus
from postgrest.exceptions import APIError
from services.SubscriptionService.app.exceptions.SubscriptionExceptions import (
    SupabaseApiFailException)
from app.services.jwt import decodeRefreshToken

class Subscriptions:
    def CreateSubscriptionRepoFunc(self,db:Client,user_id:str,order_id:str):
        """        
        :param db: supabase db instance
        :type db: Client
        :param user_id: user email
        :type user_email: str
        :param order_id
        """

        #create order in the subscription table with status - pending
        #TODO we must send user_id from getting the jwt token. but currently im getting email address, later must changed this to user_id
        
        try:
            subscription_record = db.table("Subscriptions").insert({"order_id":order_id,"user_id":user_id,"status":SubscriptionStatus.PENDING}).execute()
            return subscription_record.data[0]["order_id"]
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc
        
    def GetSubscription(self,db:Client,order_id:str):
        """
        :param order_id: valid order id from the frontend
        :type order_id: str
        """
        #? This repo function returns subscription with related to the order id.
        try:
            record = db.table("Subscriptions").select("*, Users(first_name,last_name,mobile_number,email)").eq("order_id",order_id).execute()
            if len(record.data) == 0:
                return {
                    "status":False,
                    "reason":"Order id not found"
                }
            return {
                    "status":True,
                    "data":record.data
                }
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc

subscription = Subscriptions()

