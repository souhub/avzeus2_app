from typing import List, Optional
from pydantic import BaseModel


class Floor(BaseModel):
    id: Optional[str]
    name: Optional[str]
    code: Optional[str]


class Service(BaseModel):
    name: Optional[str]
    code: Optional[str]
    floor: List[Floor]


class Site(BaseModel):
    name: Optional[str]
    code: Optional[str]
    service: List[Service]


class Result(BaseModel):
    site: List[Site]
