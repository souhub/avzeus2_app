from typing import List, Optional
from pydantic import BaseModel


class Genre(BaseModel):
    genre_id: Optional[int]
    name: Optional[str]
    ruby: Optional[str]
    list_url: Optional[str]

    # class Config:
    #     orm_mode = True


class Result(BaseModel):
    status: Optional[int]
    result_count: Optional[int]
    total_count: Optional[int]
    first_position: Optional[int]
    site_name: Optional[str]
    site_code: Optional[str]
    service_name: Optional[str]
    service_code: Optional[str]
    floor_id: Optional[int]
    floor_name: Optional[str]
    floor_code: Optional[str]
    genre: List[Genre]

    # class Config:
    #     orm_mode = True
