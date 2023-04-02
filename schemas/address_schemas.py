from typing import Optional

from pydantic import BaseModel


class AddressSchema(BaseModel):
    address1: str
    address2: Optional[str]
    city: str
    state: str
    country: str
    postal_code: str
    apt_num: Optional[int]
