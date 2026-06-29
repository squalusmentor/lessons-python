from datetime import datetime

from pydantic import BaseModel


class ArticleCreateRequest(BaseModel):
    title: str
    content: str


class ArticleUpdateRequest(BaseModel):
    title: str | None = None
    content: str | None = None


class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}
