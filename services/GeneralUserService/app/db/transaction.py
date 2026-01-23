from supabase import Client
from postgrest.exceptions import APIError
from ..exceptions.generalUserEXceptions import SupabaseApiFailException
from typing import Optional, List, Dict, Any
from typing import Final

class Transactions:
    """
    Repository layer for interacting with the database
    """
    #THis namespace created for prevent confucing property type and actual tables names of the properties features
    PROPERTY_FEATURE_NAMES : Final[dict] = {
        "Bodim":"Bording_property_features",
        "Anex":"Anex_property_features",
        "Apartment":"Apartment_property_features"
    }
    
    @staticmethod
    def FetchLandingDemoPostsRepoFunc(db: Client,limit: Optional[int] = 12) -> List[Dict[str, Any]]:
        """
        get demo 12 posts from database
        """
        try:
            all_property_count = db.table("Propeties").select("*",count="exact",head=True).execute()
            #check datbase all posts count and if count is lesser than our limit. we return all records. else we get random selected properties
            if all_property_count.count <= limit:
                data = db.from_("Propeties").select("id, property_type, price,location_name, Images(id, image)").execute()
                return data
            data = db.from_("Propeties").select("id, property_type, price, location_name,Images(id, image)").range(1,limit).execute()
            
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc
        except Exception as e:
            print(f"Error in FetchLandingDemoPostsRepoFunc: {e}")
            raise SupabaseApiFailException(message=str(e)) from e
        

    @staticmethod
    def CheckPostExistanceRepoFunc(db:Client,post_id):
        """used for check post exsistance. if post exists return true otherwise retun false"""
        try:
            property = db.table("Propeties").select("*",count="exact",head=True).eq("id",post_id).execute()
            return property
        except APIError as exc:
            print(exc)
            raise SupabaseApiFailException(message=str(exc)) from exc
        except Exception as e:
            print(f"Error in CheckPostExistanceRepoFunc: {e}")
            raise SupabaseApiFailException(message=str(e)) from e
        
    @staticmethod
    def GetPostWithIdRepoFunc(db:Client,post_id:str):
        """return property post when provide post id"""
        try:
            property_resp = db.table("Propeties").select("*,Images(id, image),Users(id,first_name,last_name),Gym(*),Hospital(*),Schools(*),Supermarket(*),Bills(*)").eq("id",post_id).execute()
            #get features according to the post id

            #check the type of the property
            property_type = property_resp.data[0]["property_type"]
            match property_type:
                case "Bodim":
                    feature_table = Transactions.PROPERTY_FEATURE_NAMES["Bodim"]
                case "Anex":
                    feature_table = Transactions.PROPERTY_FEATURE_NAMES["Anex"]
                case "Apartment":
                    feature_table = Transactions.PROPERTY_FEATURE_NAMES["Apartment"]
                case _:
                    feature_table = None

            #fetch features accoding to the features table
            features_resp = db.table(feature_table).select("*").eq("properety_id",post_id).execute()
            return property_resp,features_resp
        except APIError as exc:
            print(exc)
            raise SupabaseApiFailException(message=str(exc)) from exc
        except Exception as e:
            print(f"Error in GetPostWithIdRepoFunc: {e}")
            raise SupabaseApiFailException(message=str(e)) from e

