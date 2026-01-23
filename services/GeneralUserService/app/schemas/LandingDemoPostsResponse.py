from pydantic import BaseModel,Field
from typing import List,Optional
from fastapi import status


class ImageModel(BaseModel):
    id:str = Field(...)
    image:str = Field(...)

class PropertyModel(BaseModel):
    id:str = Field(...)
    property_type:str  = Field(...)
    price:float = Field(...)
    location_name:str = Field(...)
    Images:Optional[List[ImageModel]]

class LandingDemoPostsResponse(BaseModel):
    succuss:bool = Field(True)
    status:int = Field(status.HTTP_200_OK)
    message:Optional[str] = Field(None)
    total_available_properties:Optional[int]
    properties:Optional[List[PropertyModel]]

class LandingPageRedisPayload(BaseModel):
    total_available_properties:Optional[int]
    properties:Optional[List[PropertyModel]]
