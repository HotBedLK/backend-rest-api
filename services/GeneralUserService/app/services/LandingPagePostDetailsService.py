"""
NOTE service task : in this service i fetch limited details from post that loaded in to the landing page.
not authorized user cannot see the whole details.
"""
import pydantic
from services.GeneralUserService.app.services.GetSinglePostService import GetSinglePostService
from services.GeneralUserService.app.schemas.GetSinglePostSchema import (
    transform_landing_demo_post_details)

def GetLandingPagePostDetailsService(db,post_id):
    """    
    :param db: database instance
    :param post_id: property id
    return limited setup of property.
    also in the nearby_services object key values are randomly selected
    """
    property = GetSinglePostService(db=db,post_id=post_id)
    dto = transform_landing_demo_post_details(single_post_resp=property)
    return dto.model_dump()

    