from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from database import Base


from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


# 장소 정보
class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)

    place_name = Column(String(200), nullable=False)
    road_address = Column(String(255))
    jibun_address = Column(String(255))

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    phone = Column(String(30))
    category = Column(String(100))

    thumbnail_image = Column(String(500))

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    posts = relationship(
        "Post",
        back_populates="location",
        cascade="all, delete-orphan"
    )


# 게시글
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)

    location_id = Column(
        Integer,
        ForeignKey("locations.id"),
        nullable=False
    )

    title = Column(String(200), nullable=False)

    content = Column(Text, nullable=False)

    nickname = Column(String(30), nullable=False)

    # 평문 비밀번호 (과제용)
    password = Column(String(50), nullable=False)

    view_count = Column(Integer, default=0)

    like_count = Column(Integer, default=0)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    location = relationship(
        "Location",
        back_populates="posts"
    )

    comments = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan"
    )

    images = relationship(
        "PostImage",
        back_populates="post",
        cascade="all, delete-orphan"
    )


# 댓글
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)

    post_id = Column(
        Integer,
        ForeignKey("posts.id"),
        nullable=False
    )

    nickname = Column(String(30), nullable=False)

    content = Column(Text, nullable=False)

    # 평문 비밀번호
    password = Column(String(50), nullable=False)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    post = relationship(
        "Post",
        back_populates="comments"
    )


# 게시글 이미지
class PostImage(Base):
    __tablename__ = "post_images"

    id = Column(Integer, primary_key=True, index=True)

    post_id = Column(
        Integer,
        ForeignKey("posts.id"),
        nullable=False
    )

    image_url = Column(String(500), nullable=False)

    sort_order = Column(Integer, default=0)

    post = relationship(
        "Post",
        back_populates="images"
    )