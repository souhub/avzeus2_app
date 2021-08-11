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
    id: Optional[int]
    name: Optional[str]
    ruby: Optional[str]
    bust: Optional[int]
    cup: Optional[str]
    waist: Optional[int]
    hip: Optional[int]
    height: Optional[int]
    birthday: Optional[str]
    blood_type: Optional[str]
    hobby: Optional[str]
    prefectures: Optional[str]
    image_url: Optional[ImageUrl]
    list_url: Optional[ListUrl]


class Result(BaseModel):
    status: int
    result_count: int
    total_count: int
    first_position: int
    actress: Optional[List[Actress]]
