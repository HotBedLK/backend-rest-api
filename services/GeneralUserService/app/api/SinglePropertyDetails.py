from fastapi import APIRouter
from services.AdminService.app.main import app
from fastapi import Depends
from typing import Annotated
from supabase import Client
from app.database.supabase import get_supabase_client
from services.GeneralUserService.app.services.GetSinglePostService import GetSinglePostService
from services.GeneralUserService.app.schemas.GetSinglePostSchema import SinglePostResponse

router  = APIRouter(tags=["General user routes"])

#used for get single property post details required post id from the frontend
@router.get(path="/post-details/{post_id}",description="This endpoint used for fetch single post details")
def GetSinglePostController(db: Annotated[Client, Depends(get_supabase_client)],post_id:str):
    post =  GetSinglePostService(db=db,post_id=post_id)
    return SinglePostResponse(data=post.data)