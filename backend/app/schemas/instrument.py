import uuid

from pydantic import BaseModel


class InstrumentBase(BaseModel):
    name: str
    slug: str


class InstrumentCreate(InstrumentBase):
    pass


class InstrumentResponse(InstrumentBase):
    id: uuid.UUID

    model_config = {"from_attributes": True}