from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from pydantic import Field  

# Response models
class TitleResponse(BaseModel):
    titles: List[str]


class StoryResponse(BaseModel):
    stories: List[str]


class GeneratedContent(BaseModel):
    success: bool
    data: dict
    message: str


class Product(BaseModel):
    name: str = Field(..., description="Product name")
    category: str = Field(
        ...,
        description="Category of the product",
        pattern="^(textile|pottery|furniture|jewellery|decorative work|home utilities)$",
    )
    location: str
    description: Optional[str] = ""
    title: Optional[str] = ""
    story: Optional[str] = ""
    caption: Optional[str] = ""
    hashtags: List[str] = []
    seo_tags: List[str] = []
    images: List[str] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
