from services.GeneralUserService.app.db.transaction import  Transactions
from services.CashingService.GeneralUserServiceCache import GeneralUserCacheStorage
from services.GeneralUserService.app.schemas.LandingDemoPostsResponse import LandingPageRedisPayload



#service layer for get 12 random posts from the database
def FetchLandingDemoPostsService(db):
    #check in the cache allready available
    cached = GeneralUserCacheStorage.GetLandingPageDemos()
    if cached is None:
        #call repo layer and get 12 posts
        payload =  Transactions.FetchLandingDemoPostsRepoFunc(db=db,limit=12)
        #store in the redis cache memory
        GeneralUserCacheStorage.SetLandingPageDemos(payload=LandingPageRedisPayload(total_available_properties=len(payload.data),properties=payload.data))
        cached = GeneralUserCacheStorage.GetLandingPageDemos()
        return cached
    return cached

    
    
    
    

    
