
from datetime import datetime
from typing import Any, List, Optional, Tuple
from pydantic import BaseModel, Field, ConfigDict
import random




class ImageRow(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    image: str


class UserRow(BaseModel):
    model_config = ConfigDict(extra="ignore")
    first_name: str
    last_name: str


class PropertyRow(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    location_name: str
    price: int
    user_id: Optional[str] = None

    actual_log: Optional[str] = None
    actual_lat: Optional[str] = None
    selected_lat: Optional[str] = None
    selected_log: Optional[str] = None

    description: str
    created_at: datetime
    property_type: str

    location_city: str
    location_district: str

    availability: bool
    available_date: datetime

    Images: List[ImageRow] = Field(default_factory=list)
    Users: Optional[UserRow] = None

    Gym: List[Any] = Field(default_factory=list)
    Hospital: List[Any] = Field(default_factory=list)
    Schools: List[Any] = Field(default_factory=list)
    Supermarket: List[Any] = Field(default_factory=list)
    Bills: List[Any] = Field(default_factory=list)


class BodimFeatureRow(BaseModel):
    model_config = ConfigDict(extra="ignore")

    attach_bathroom_count: int
    seperate_bathroom_count: int
    parking: bool
    bed_count: int
    table: int
    mirror_table: int
    storagebox: int
    fan: int
    clothingrack: int


class FeaturesEnvelope(BaseModel):
    model_config = ConfigDict(extra="ignore")
    data: List[BodimFeatureRow] = Field(default_factory=list)
    count: Optional[int] = None


class PropertyDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    location_name: str
    price: int
    description: str
    created_at: datetime
    property_type: str
    availability: bool
    available_date: datetime
    location_city: str
    location_district: str

    actual_log: Optional[str] = None
    actual_lat: Optional[str] = None
    selected_lat: Optional[str] = None
    selected_log: Optional[str] = None


class GymItem(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str = ""
    distance: float = 0.0
    location: str = ""


class HospitalItem(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str = ""
    distance: float = 0.0
    location: str = ""


class SchoolItem(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str = ""
    distance: float = 0.0
    location: str = ""


class SupermarketItem(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str = ""
    distance: float = 0.0
    location: str = ""


class BillsItem(BaseModel):
    model_config = ConfigDict(extra="ignore")
    water_bill: bool = False
    electricity_bill: bool = False
    parking_bill: bool = False
    internet_bill: bool = False
    tv_bill: bool = False
    service_bill: bool = False


class NearbyServicesDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")

    Gym: List[GymItem] = Field(default_factory=list)
    Hospital: List[HospitalItem] = Field(default_factory=list)
    Schools: List[SchoolItem] = Field(default_factory=list)
    Supermarket: List[SupermarketItem] = Field(default_factory=list)
    Bills: List[BillsItem] = Field(default_factory=list)


class SinglePostDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")

    property: PropertyDTO
    property_features: Optional[BodimFeatureRow] = None
    nearby_services: NearbyServicesDTO
    owner_of_the_property: Optional[UserRow] = None
    property_images: List[ImageRow] = Field(default_factory=list)


class SinglePostResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    data: List[SinglePostDTO]
    count: Optional[int] = None



def _unwrap_resp(resp: Any) -> Tuple[List[Any], Optional[int]]:
    if hasattr(resp, "data"):
        return (resp.data or []), getattr(resp, "count", None)
    if isinstance(resp, dict):
        return resp.get("data", []) or [], resp.get("count")
    return [], None


def _build_single_post(property_obj: PropertyRow, feature_obj: Optional[BodimFeatureRow]) -> SinglePostDTO:
    prop_dto = PropertyDTO(
        id=property_obj.id,
        location_name=property_obj.location_name,
        price=property_obj.price,
        description=property_obj.description,
        created_at=property_obj.created_at,
        property_type=property_obj.property_type,
        availability=property_obj.availability,
        available_date=property_obj.available_date,
        location_city=property_obj.location_city,
        location_district=property_obj.location_district,
        actual_log=property_obj.actual_log,
        actual_lat=property_obj.actual_lat,
        selected_lat=property_obj.selected_lat,
        selected_log=property_obj.selected_log,
    )

    nearby = NearbyServicesDTO.model_validate(
        {
            "Gym": property_obj.Gym,
            "Hospital": property_obj.Hospital,
            "Schools": property_obj.Schools,
            "Supermarket": property_obj.Supermarket,
            "Bills": property_obj.Bills,
        }
    )

    return SinglePostDTO(
        property=prop_dto,
        property_features=feature_obj,
        nearby_services=nearby,
        owner_of_the_property=property_obj.Users,
        property_images=property_obj.Images,
    )


def transform_combined_payload(resp: Any) -> SinglePostResponse:
    raw_list, count = _unwrap_resp(resp)
    if not raw_list:
        return SinglePostResponse(data=[], count=count)

    property_obj = PropertyRow.model_validate(raw_list[0])

    feature_obj: Optional[BodimFeatureRow] = None
    if len(raw_list) >= 2 and isinstance(raw_list[1], dict) and "data" in raw_list[1]:
        env = FeaturesEnvelope.model_validate(raw_list[1])
        feature_obj = env.data[0] if env.data else None

    post = _build_single_post(property_obj, feature_obj)
    return SinglePostResponse(data=[post], count=count)


def transform_separate_responses(property_resp: Any, features_resp: Any) -> SinglePostResponse:
    prop_list, prop_count = _unwrap_resp(property_resp)
    if not prop_list:
        return SinglePostResponse(data=[], count=prop_count)

    property_obj = PropertyRow.model_validate(prop_list[0])

    feat_list, _ = _unwrap_resp(features_resp)

    feature_obj: Optional[BodimFeatureRow] = None
    if feat_list and isinstance(feat_list[0], dict) and "attach_bathroom_count" in feat_list[0]:
        feature_obj = BodimFeatureRow.model_validate(feat_list[0])

    elif feat_list and isinstance(feat_list[0], dict) and "data" in feat_list[0]:
        env = FeaturesEnvelope.model_validate(feat_list[0])
        feature_obj = env.data[0] if env.data else None

    post = _build_single_post(property_obj, feature_obj)
    return SinglePostResponse(data=[post], count=prop_count)





class PropertyCardDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")
    location_name: str
    price: int


class NearbyServicesRandomDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")

    Gym: List[Any] = Field(default_factory=list)
    Hospital: List[Any] = Field(default_factory=list)
    Schools: List[Any] = Field(default_factory=list)
    Supermarket: List[Any] = Field(default_factory=list)
    Bills: List[Any] = Field(default_factory=list)


class LandingDemoPostDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")

    property: PropertyCardDTO
    owner_of_the_property: Optional[UserRow] = None  
    nearby_services: NearbyServicesRandomDTO


class LandingDemoPostsResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    data: List[LandingDemoPostDTO] = Field(default_factory=list)
    count: Optional[int] = None


def _pick_one(items: Any) -> List[Any]:
    """
    Picks one random element from a list and returns it as a single-item list.
    Returns [] if items is None, not a list, or empty.
    """
    if not items or not isinstance(items, list):
        return []
    return [random.choice(items)] if items else []


def _build_landing_demo_post(property_obj: PropertyRow) -> LandingDemoPostDTO:
    """
    Builds the limited DTO for landing/demo posts:
      - property: location_name, price
      - owner_of_the_property: first_name, last_name (via UserRow)
      - nearby_services: ONE random item per category
    """
    prop_card = PropertyCardDTO(
        location_name=property_obj.location_name,
        price=property_obj.price,
    )

    nearby_random = NearbyServicesRandomDTO.model_validate(
        {
            "Gym": _pick_one(property_obj.Gym),
            "Hospital": _pick_one(property_obj.Hospital),
            "Schools": _pick_one(property_obj.Schools),
            "Supermarket": _pick_one(property_obj.Supermarket),
            "Bills": _pick_one(property_obj.Bills),
        }
    )

    return LandingDemoPostDTO(
        property=prop_card,
        owner_of_the_property=property_obj.Users,
        nearby_services=nearby_random,
    )


def transform_landing_demo_posts(property_resp: Any) -> LandingDemoPostsResponse:
    """
    Transformer for the new landing/demo endpoint.
    Expects a response like:
    """
    raw_list, count = _unwrap_resp(property_resp)  

    if not raw_list:
        return LandingDemoPostsResponse(data=[], count=count)

    posts: List[LandingDemoPostDTO] = []
    for row in raw_list:
        property_obj = PropertyRow.model_validate(row)
        posts.append(_build_landing_demo_post(property_obj))

    return LandingDemoPostsResponse(data=posts, count=count)


def transform_landing_demo_post_details(single_post_resp: Any) -> LandingDemoPostsResponse:
    """
    Accepts:
      - SinglePostResponse (your existing response model)
      - or dict shaped like {"data":[...], "count":...}
    """

    raw_list, count = _unwrap_resp(single_post_resp)  

    if not raw_list:
        return LandingDemoPostsResponse(data=[], count=count)

    first = raw_list[0]

    if hasattr(first, "property"):
        prop = first.property
        owner = getattr(first, "owner_of_the_property", None)
        nearby = getattr(first, "nearby_services", None)

        nearby_random = NearbyServicesRandomDTO.model_validate(
            {
                "Gym": _pick_one(getattr(nearby, "Gym", [])),
                "Hospital": _pick_one(getattr(nearby, "Hospital", [])),
                "Schools": _pick_one(getattr(nearby, "Schools", [])),
                "Supermarket": _pick_one(getattr(nearby, "Supermarket", [])),
                "Bills": _pick_one(getattr(nearby, "Bills", [])),
            }
        )

        post = LandingDemoPostDTO(
            property=PropertyCardDTO(
                location_name=getattr(prop, "location_name", ""),
                price=getattr(prop, "price", 0),
            ),
            owner_of_the_property=owner,
            nearby_services=nearby_random,
        )
        return LandingDemoPostsResponse(data=[post], count=count)

    if isinstance(first, dict):
        prop_dict = first.get("property") or {}
        owner_dict = first.get("owner_of_the_property")
        nearby_dict = first.get("nearby_services") or {}

        nearby_random = NearbyServicesRandomDTO.model_validate(
            {
                "Gym": _pick_one(nearby_dict.get("Gym", [])),
                "Hospital": _pick_one(nearby_dict.get("Hospital", [])),
                "Schools": _pick_one(nearby_dict.get("Schools", [])),
                "Supermarket": _pick_one(nearby_dict.get("Supermarket", [])),
                "Bills": _pick_one(nearby_dict.get("Bills", [])),
            }
        )

        post = LandingDemoPostDTO(
            property=PropertyCardDTO(
                location_name=prop_dict.get("location_name", ""),
                price=prop_dict.get("price", 0),
            ),
            owner_of_the_property=UserRow.model_validate(owner_dict) if owner_dict else None,
            nearby_services=nearby_random,
        )
        return LandingDemoPostsResponse(data=[post], count=count)

    # Unknown shape
    return LandingDemoPostsResponse(data=[], count=count)

