from fastapi import APIRouter
from supabase import Client
from typing import Annotated
from fastapi import Depends
from app.database.supabase import get_supabase_client
from services.GeneralUserService.app.services.FetchLandingDemoPostsService import (
    FetchLandingDemoPostsService)
from services.GeneralUserService.app.schemas.LandingDemoPostsResponse import (
    LandingDemoPostsResponse)

router  = APIRouter(tags=["General user routes"])

#route for get random 12 post from the database
@router.get("/landing-feed",description="get random 12 post from the database",response_model=LandingDemoPostsResponse)
def register(db: Annotated[Client, Depends(get_supabase_client)]):
    demo_properties = FetchLandingDemoPostsService(db=db)
    return LandingDemoPostsResponse(
        succuss=True,
        message="Landng page post retrived succuss!",
        total_available_properties=demo_properties.total_available_properties,
        properties=demo_properties.properties
    ) 
