from pydantic import BaseModel, Extra, Field, PositiveInt

from app.schemas.base import AbstractBaseSchema


class CreateCharityProject(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(CreateCharityProject):
    name: str = Field(None, min_length=1, max_length=100)
    description: str = Field(None, min_length=1)
    full_amount: PositiveInt = Field(None)

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CreateCharityProject, AbstractBaseSchema):
    id: int

    class Config:
        orm_mode = True
