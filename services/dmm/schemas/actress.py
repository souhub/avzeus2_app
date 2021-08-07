from typing import List, Optional
from pydantic import BaseModel


class ListUrl(BaseModel):
    digital: Optional[str]
    monthly_premium: Optional[str]
    mono: Optional[str]
    rental: Optional[str]


class ImageUrl(BaseModel):
    small: Optional[str]
    large: Optional[str]


class Actress(BaseModel):
    id: Optional[str]
    name: Optional[str]
    ruby: Optional[str]
    bust: Optional[str]
    cup: Optional[str]
    waist: Optional[str]
    hip: Optional[str]
    height: Optional[str]
    birthday: Optional[str]
    blood_type: Optional[str]
    hobby: Optional[str]
    prefectures: Optional[str]
    image_url: Optional[ImageUrl]
    list_url: Optional[ListUrl]


class Result(BaseModel):
    status: str
    result_count: int
    total_count: str
    first_position: int
    actress: List[Actress]
