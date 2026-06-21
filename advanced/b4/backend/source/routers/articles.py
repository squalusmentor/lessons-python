from typing import List

from fastapi import APIRouter, Request, HTTPException

from source.schemas.article import ArticleCreateRequest, ArticleUpdateRequest, ArticleResponse
import source.handlers.articles as articles_handler

router = APIRouter()


@router.get("", response_model=List[ArticleResponse])
async def get_articles(request: Request):
    result = await articles_handler.get_articles(request)
    if result is False:
        raise HTTPException(status_code=500, detail="Unexpected error")
    return result


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(article_id: int, request: Request):
    result = await articles_handler.get_article(article_id, request)
    if result is False:
        raise HTTPException(status_code=500, detail="Unexpected error")
    return result


@router.post("", response_model=ArticleResponse)
async def create_article(body: ArticleCreateRequest, request: Request):
    result = await articles_handler.create_article(body, request)
    if result is False:
        raise HTTPException(status_code=500, detail="Unexpected error")
    return result


@router.put("/{article_id}", response_model=ArticleResponse)
async def update_article(article_id: int, body: ArticleUpdateRequest, request: Request):
    result = await articles_handler.update_article(article_id, body, request)
    if result is False:
        raise HTTPException(status_code=500, detail="Unexpected error")
    return result


@router.delete("/{article_id}")
async def delete_article(article_id: int, request: Request):
    result = await articles_handler.delete_article(article_id, request)
    if result is False:
        raise HTTPException(status_code=500, detail="Unexpected error")
    return result
