from fastapi import APIRouter,Depends
from typing import Annotated
from supabase import Client
from app.database.supabase import get_supabase_client
from services.GeneralUserService.app.services.LandingPagePostDetailsService import (
    GetLandingPagePostDetailsService)


"""
NOTE controller task : in this controller i fetch limited details from post that loaded in to the landing page.
not authorized user cannot see the whole details. this endpoint only returns limited setup of details only 
"""

router  = APIRouter(tags=["General user routes"])

@router.get("/landing-feed-post-details/{property_id}",description="this return landing page properties details with limited setup")
def PostDetailsController(property_id:str,db: Annotated[Client, Depends(get_supabase_client)]):
    return GetLandingPagePostDetailsService(db=db,post_id=property_id)

