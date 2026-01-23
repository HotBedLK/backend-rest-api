from services.GeneralUserService.app.db.transaction import  Transactions
from services.GeneralUserService.app.utils import utils
from services.GeneralUserService.app.exceptions.generalUserEXceptions import (
    GeneralUserCacheStorageException, GeneralUserServiceLayerException,
    NotAcceptablePostIDException, NotExsistPropertyException)
from services.GeneralUserService.app.schemas.GetSinglePostSchema import transform_separate_responses
from services.CashingService.GeneralUserServiceCache import GeneralUserCacheStorage

#service layer for GetSinglePostController
def GetSinglePostService(db,post_id):
    try:
        #check the post id is a valid id
        if not utils.IsValidModelId(expected_uuid=post_id):
            raise NotAcceptablePostIDException(message="this post id is invalid. can't process!")

        #check in the redis memory that post is available
        cached = GeneralUserCacheStorage.GetProperty(property_id=post_id)
        if cached is not None:
            return cached

        #if not fetch it from databse
        #check that post is exists in the database
        post_count = Transactions.CheckPostExistanceRepoFunc(db=db,post_id=post_id)
        if post_count.count == 1:
            """when excute when post is available. and we refetch the post with whole details and cached it and return"""
            property_resp,features_resp =  Transactions.GetPostWithIdRepoFunc(db=db,post_id=post_id)
            out = transform_separate_responses(property_resp, features_resp)
            #cache the property
            if GeneralUserCacheStorage.SetProperty(payload=out):
                return GeneralUserCacheStorage.GetProperty(property_id=post_id)
            else:
                GeneralUserCacheStorageException(message="Something went wrong")
        else:
            #if no any post reference to user sended
            raise NotExsistPropertyException(message="This post cannot be found!")
    except NotExsistPropertyException:
        raise
    except NotAcceptablePostIDException:
        raise
    except Exception:
        raise GeneralUserServiceLayerException(message="Something went wrong in our end!")
        