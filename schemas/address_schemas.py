from pydantic import BaseModel


class AddressSchema(BaseModel):
    address1: str
    address2: str | None = None
    city: str
    state: str
    country: str
    postal_code: str
    apt_num: int | None = None
