from pydantic import BaseModel, Field


class CategoryDisplay(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=50)