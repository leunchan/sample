from __future__ import annotations

from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, Field


class LocationBase(BaseModel):
    place_name: str = Field(...)
    road_address: Optional[str] = None
    jibun_address: Optional[str] = None
    latitude: float
    longitude: float
    phone: Optional[str] = None
    category: Optional[str] = None
    thumbnail_image: Optional[str] = None


class LocationCreate(LocationBase):
    pass


class LocationResponse(LocationBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class PostImageBase(BaseModel):
    image_url: str
    sort_order: Optional[int] = 0


class PostImageCreate(PostImageBase):
    pass


class PostImageResponse(PostImageBase):
    id: int
    post_id: int

    model_config = {"from_attributes": True}


class CommentBase(BaseModel):
    nickname: str
    content: str
    password: str


class CommentCreate(CommentBase):
    post_id: int


class CommentResponse(BaseModel):
    id: int
    post_id: int
    nickname: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class PostBase(BaseModel):
    location_id: int
    title: str
    content: str
    nickname: str
    password: str


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    password: str


class PostResponse(PostBase):
    id: int
    view_count: int
    like_count: int
    created_at: datetime
    updated_at: Optional[datetime]
    images: List[PostImageResponse] = []
    comments: List[CommentResponse] = []

    model_config = {"from_attributes": True}
