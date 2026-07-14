from __future__ import annotations

from typing import Any
from uuid import uuid4

import uvicorn
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Team Project Backend", version="2.0.0")


class PostCreate(BaseModel):
    title: str = Field(min_length=1)
    content: str = Field(min_length=1)
    password: str = Field(min_length=1)
    tags: list[str] = Field(default_factory=list)


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    password: str = Field(min_length=1)
    tags: list[str] | None = None


class PostVerify(BaseModel):
    password: str = Field(min_length=1)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    session_id: str | None = None


class DirectionsRequest(BaseModel):
    origin: str
    destination: str
    waypoints: list[str] = Field(default_factory=list)


class PostRecord(dict[str, Any]):
    pass


posts: list[dict[str, Any]] = [
    {
        "id": 1,
        "title": "첫 번째 게시글",
        "content": "FastAPI 백엔드 초기 예시입니다.",
        "password": "1234",
        "tags": ["fastapi", "backend"],
        "view_count": 3,
        "like_count": 2,
        "bookmark_count": 1,
        "liked": False,
        "bookmarked": False,
    }
]

chat_sessions: dict[str, list[dict[str, str]]] = {}

locations: list[dict[str, Any]] = [
    {
        "id": 1,
        "category": "tourist",
        "name": "해변 산책로",
        "description": "바다 전망이 좋은 관광 명소입니다.",
        "address": "부산 해운대구",
        "latitude": 35.1587,
        "longitude": 129.1604,
    },
    {
        "id": 2,
        "category": "restaurant",
        "name": "바다횟집",
        "description": "해산물 전문 음식점입니다.",
        "address": "부산 해운대구 우동",
        "latitude": 35.1590,
        "longitude": 129.1608,
    },
    {
        "id": 3,
        "category": "festival",
        "name": "여름 밤 축제",
        "description": "야간 공연과 먹거리 축제가 열립니다.",
        "address": "부산 광안리",
        "latitude": 35.1532,
        "longitude": 129.1186,
    },
]


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Backend server is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/posts")
def list_posts(page: int = 1, size: int = 10, keyword: str | None = None) -> dict[str, Any]:
    filtered = [post for post in posts if not keyword or keyword.lower() in " ".join([post["title"], post["content"], " ".join(post["tags"])]).lower()]
    start = (page - 1) * size
    end = start + size
    return {
        "items": filtered[start:end],
        "page": page,
        "size": size,
        "total": len(filtered),
    }


@app.get("/api/posts/{post_id}")
def get_post(post_id: int) -> dict[str, Any]:
    post = next((item for item in posts if item["id"] == post_id), None)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    post["view_count"] += 1
    return post


@app.post("/api/posts", status_code=201)
def create_post(payload: PostCreate) -> dict[str, Any]:
    post = {
        "id": (posts[-1]["id"] + 1) if posts else 1,
        "title": payload.title,
        "content": payload.content,
        "password": payload.password,
        "tags": payload.tags,
        "view_count": 0,
        "like_count": 0,
        "bookmark_count": 0,
        "liked": False,
        "bookmarked": False,
    }
    posts.append(post)
    return post


@app.put("/api/posts/{post_id}")
def update_post(post_id: int, payload: PostUpdate) -> dict[str, Any]:
    post = next((item for item in posts if item["id"] == post_id), None)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if post["password"] != payload.password:
        raise HTTPException(status_code=403, detail="Invalid password")
    if payload.title is not None:
        post["title"] = payload.title
    if payload.content is not None:
        post["content"] = payload.content
    if payload.tags is not None:
        post["tags"] = payload.tags
    return post


@app.delete("/api/posts/{post_id}")
def delete_post(post_id: int, password: str = Query(...)) -> dict[str, str]:
    post = next((item for item in posts if item["id"] == post_id), None)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if post["password"] != password:
        raise HTTPException(status_code=403, detail="Invalid password")
    posts.remove(post)
    return {"message": "Post deleted"}


@app.post("/api/posts/{post_id}/verify")
def verify_post_password(post_id: int, payload: PostVerify) -> dict[str, bool]:
    post = next((item for item in posts if item["id"] == post_id), None)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"verified": post["password"] == payload.password}


@app.post("/api/posts/{post_id}/like")
def toggle_like(post_id: int) -> dict[str, Any]:
    post = next((item for item in posts if item["id"] == post_id), None)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    post["liked"] = not post["liked"]
    post["like_count"] = max(0, post["like_count"] + (1 if post["liked"] else -1))
    return {"liked": post["liked"], "like_count": post["like_count"]}


@app.post("/api/posts/{post_id}/bookmark")
def toggle_bookmark(post_id: int) -> dict[str, Any]:
    post = next((item for item in posts if item["id"] == post_id), None)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    post["bookmarked"] = not post["bookmarked"]
    post["bookmark_count"] = max(0, post["bookmark_count"] + (1 if post["bookmarked"] else -1))
    return {"bookmarked": post["bookmarked"], "bookmark_count": post["bookmark_count"]}


@app.post("/api/chat")
def create_chat_message(payload: ChatRequest) -> dict[str, Any]:
    session_id = payload.session_id or str(uuid4())
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []
    user_message = {"role": "user", "content": payload.message}
    assistant_message = {"role": "assistant", "content": f"요청하신 내용에 대한 답변을 준비했습니다: {payload.message}"}
    chat_sessions[session_id].extend([user_message, assistant_message])
    return {"session_id": session_id, "messages": [user_message, assistant_message]}


@app.get("/api/chat/sessions/{session_id}/messages")
def get_chat_messages(session_id: str) -> dict[str, Any]:
    if session_id not in chat_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"session_id": session_id, "messages": chat_sessions[session_id]}


@app.get("/api/locations")
def list_locations(category: str | None = None, keyword: str | None = None) -> dict[str, Any]:
    filtered = locations
    if category:
        filtered = [item for item in filtered if item["category"].lower() == category.lower()]
    if keyword:
        filtered = [item for item in filtered if keyword.lower() in item["name"].lower() or keyword.lower() in item["description"].lower()]
    return {"items": filtered, "total": len(filtered)}


@app.get("/api/locations/{location_id}")
def get_location(location_id: int) -> dict[str, Any]:
    location = next((item for item in locations if item["id"] == location_id), None)
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@app.get("/api/locations/{location_id}/coordinates")
def get_location_coordinates(location_id: int) -> dict[str, Any]:
    location = next((item for item in locations if item["id"] == location_id), None)
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return {"location_id": location_id, "latitude": location["latitude"], "longitude": location["longitude"]}


@app.get("/api/restaurants")
def list_restaurants(keyword: str | None = None, lat: float | None = None, lng: float | None = None, radius: int = 1000) -> dict[str, Any]:
    items = [
        {
            "place_id": f"place-{index}",
            "name": f"맛집 {index}",
            "address": "샘플 주소",
            "rating": 4.5,
            "latitude": (lat or 35.15) + index * 0.001,
            "longitude": (lng or 129.16) + index * 0.001,
            "radius": radius,
        }
        for index in range(1, 4)
    ]
    if keyword:
        items = [item for item in items if keyword.lower() in item["name"].lower()]
    return {"items": items, "total": len(items)}


@app.get("/api/restaurants/{place_id}")
def get_restaurant_detail(place_id: str) -> dict[str, Any]:
    return {
        "place_id": place_id,
        "name": "샘플 음식점",
        "rating": 4.7,
        "opening_hours": ["09:00-22:00"],
        "photos": ["https://example.com/photo.jpg"],
    }


@app.post("/api/directions")
def get_directions(payload: DirectionsRequest) -> dict[str, Any]:
    return {
        "origin": payload.origin,
        "destination": payload.destination,
        "waypoints": payload.waypoints,
        "polyline": "u~eF~s`vM~s`vM~s`vM",
        "distance_meters": 3200,
        "duration_seconds": 900,
    }


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
