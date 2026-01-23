from redis import Redis
from functools import lru_cache
from decouple import config
from services.GeneralUserService.app.schemas.LandingDemoPostsResponse import LandingPageRedisPayload
import json
from typing import Final
from app.utils.rate_limiter import get_redis_client
from services.GeneralUserService.app.schemas.GetSinglePostSchema import SinglePostResponse
from services.GeneralUserService.app.exceptions.generalUserEXceptions import (
    GeneralUserCacheStorageException)

@lru_cache(maxsize=1)
def GetGeneralUserRedisClient()->Redis:
    """each service have different redis instances. so for each service have separate databases
            for this service we used database 1
        """
    return Redis(
        
        host=config("REDIS_HOST", default="redis_database"),
        port=config("REDIS_PORT", default=6379, cast=int),
        password=config("REDIS_PASSWORD", default=None),
        db=1, 
        decode_responses=True,
    )

class GeneralUserCacheStorage:

    LANDING_PAGE_DEMO_KEY:Final[str] = "landing:properties"
    LANDING_PAGE_DEMO_TTL :Final[int] =  600
    POST_STORE_TTL = 60

    @staticmethod
    def SetLandingPageDemos(payload:LandingPageRedisPayload)->bool:
        """store lading page demo post array in to the redis database-1 redis database-1 beongs only to general user service only!!!"""
        try:
            row_payload = payload.model_dump(exclude_none=True,mode="json")
            r:Redis = GetGeneralUserRedisClient()
            r.setex(GeneralUserCacheStorage.LANDING_PAGE_DEMO_KEY,GeneralUserCacheStorage.LANDING_PAGE_DEMO_TTL,json.dumps(row_payload))
            return True
        except Exception as e:
            print("something happend on StoreLandingPageDemos function",e)
            raise GeneralUserCacheStorageException(message="Something went wrong")
        
    @staticmethod
    def GetLandingPageDemos():
        """Get stored landing page demo posts from redis database-1"""
        try:
            r:Redis = GetGeneralUserRedisClient()
            cached = r.get(GeneralUserCacheStorage.LANDING_PAGE_DEMO_KEY)
            if not cached:
                return None
            data = json.loads(cached)
            return LandingPageRedisPayload.model_validate(data)
        except Exception as e:
            print("something happend on GetLandingPageDemos function",e)
            raise GeneralUserCacheStorageException(message="Something went wrong")

    @staticmethod
    def SetProperty(payload:SinglePostResponse):
        """
        NOTE : in this we store property with the property id. ttl = 60s
        :payload type must be SinglePostResponse model
        """
        try:
            r:Redis = GetGeneralUserRedisClient()
            row_payload = payload.model_dump(exclude_none=True,mode="json")
            key = payload.data[0].property.id
            ok = r.setex(key,GeneralUserCacheStorage.POST_STORE_TTL,json.dumps(row_payload))
            if ok:
                return ok
            return not ok
        except Exception as e:
            print("something happend on SetProperty function",e)
            raise GeneralUserCacheStorageException(message="Something went wrong")
        
    @staticmethod
    def GetProperty(property_id):
        """
        :param property_id: valid property id
        this return cached property if available else return None
        """
        try:
            r:Redis = GetGeneralUserRedisClient()
            cached = r.get(property_id)
            if not cached:
                return None
            data = json.loads(cached)
            return SinglePostResponse.model_validate(data)
        except Exception as e:
            print("something happend on GetLandingPageDemos function",e)
            raise GeneralUserCacheStorageException(message="Something went wrong")






        


