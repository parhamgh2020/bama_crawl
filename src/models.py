from typing import Union, List
from pydantic import BaseModel


class PriceInfo(BaseModel):
    type: str
    price: int


class Media(BaseModel):
    images: List[dict]


class AdvertiseModel(BaseModel):
    link: str
    id: Union[str, int]
    id_str: str
    title: str
    spec: dict
    price_info: PriceInfo
    text: str
    numbers: list
    published_date: str
    location: str
    user: dict
    media: Media

