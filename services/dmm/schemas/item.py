from typing import Counter, List, Optional
from pydantic import BaseModel


class Size(BaseModel):
    id: Optional[int]
    name: Optional[str]


class Color(BaseModel):
    id: Optional[int]
    name: Optional[str]


class Type(BaseModel):
    id: Optional[int]
    name: Optional[str]


class Label(BaseModel):
    id: Optional[int]
    name: Optional[str]


class Author(BaseModel):
    id: Optional[int]
    name: Optional[str]


class Director(BaseModel):
    id: Optional[int]
    name: Optional[str]


class Actress(BaseModel):
    id: Optional[int]
    name: Optional[str]
    ruby: Optional[str]
    image: Optional[str]


class Actor(BaseModel):
    id: Optional[int]
    name: Optional[str]


class Maker(BaseModel):
    id: Optional[int]
    name: Optional[str]


class Series(BaseModel):
    id: Optional[int]
    name: Optional[str]


class Genre(BaseModel):
    id: Optional[int]
    name: Optional[str]


class ItemInfo(BaseModel):
    genre: Optional[List[Genre]]
    series: Optional[List[Series]]
    maker: Optional[List[Maker]]
    actor: Optional[List[Actor]]
    actress: Optional[List[Actress]]
    director: Optional[List[Director]]
    author: Optional[List[Author]]
    label: Optional[List[Label]]
    type: Optional[List[Type]]
    color: Optional[List[Color]]
    size: Optional[List[Size]]


class SampleMovieURL(BaseModel):
    size_476_306: Optional[str]
    size_560_360: Optional[str]
    size_644_414: Optional[str]
    size_720_480: Optional[str]
    pc_flag: Optional[int]
    sp_flag: Optional[str]


class ImageURL(BaseModel):
    list: Optional[str]
    small: Optional[str]
    large: Optional[str]


class Review(BaseModel):
    count: Optional[int]
    average: Optional[float]


class Item(BaseModel):
    service_code: Optional[str]
    service_name: Optional[str]
    floor_code: Optional[str]
    floor_name: Optional[str]
    category_name: Optional[str]
    content_id: Optional[str]
    product_id: Optional[str]
    title: Optional[str]
    volume: Optional[int]
    number: Optional[int]
    review: Optional[Review]
    URL: Optional[str]
    affiliateURL: Optional[str]
    URLsp: Optional[str]
    affiliateURLsp: Optional[str]
    imageURL: Optional[ImageURL]
    sampleMovieURL: Optional[SampleMovieURL]
    iteminfo: Optional[ItemInfo]
    jancode: Optional[str]
    maker_product: Optional[str]
    isbn: Optional[str]
    stock: Optional[str]


class Result(BaseModel):
    status: Optional[int]
    result_count: Optional[int]
    total_count: Optional[int]
    items: List[Item]
