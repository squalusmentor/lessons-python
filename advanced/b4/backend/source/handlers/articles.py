from fastapi import Request, HTTPException
from sqlalchemy import select

from source.db_connect import async_session
from source.models.article import Article
from source.models.user import User
from source.schemas.article import ArticleCreateRequest, ArticleUpdateRequest
from source.services.decorators import handle_errors_async
from source.services.scripts import decode_token


def _get_current_user_id(request: Request) -> int:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user_id = decode_token(token)
    if user_id is False:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user_id


@handle_errors_async
async def get_articles(request: Request):
    current_user_id = _get_current_user_id(request)

    async with async_session() as session:
        current_user = await session.get(User, current_user_id)
        if not current_user or not current_user.is_active:
            raise HTTPException(status_code=401, detail="Not authenticated")

        if current_user.is_admin:
            result = await session.scalars(select(Article))
        else:
            result = await session.scalars(
                select(Article).where(Article.owner_id == current_user_id)
            )
        articles = result.all()

    return articles


@handle_errors_async
async def get_article(article_id: int, request: Request):
    current_user_id = _get_current_user_id(request)

    async with async_session() as session:
        current_user = await session.get(User, current_user_id)
        if not current_user or not current_user.is_active:
            raise HTTPException(status_code=401, detail="Not authenticated")

        article = await session.get(Article, article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")

        if article.owner_id != current_user_id and not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Forbidden")

    return article


@handle_errors_async
async def create_article(body: ArticleCreateRequest, request: Request):
    current_user_id = _get_current_user_id(request)

    async with async_session() as session:
        current_user = await session.get(User, current_user_id)
        if not current_user or not current_user.is_active:
            raise HTTPException(status_code=401, detail="Not authenticated")

        article = Article(
            title=body.title,
            content=body.content,
            owner_id=current_user_id,
        )
        session.add(article)
        await session.commit()
        await session.refresh(article)

    return article


@handle_errors_async
async def update_article(article_id: int, body: ArticleUpdateRequest, request: Request):
    current_user_id = _get_current_user_id(request)

    async with async_session() as session:
        current_user = await session.get(User, current_user_id)
        if not current_user or not current_user.is_active:
            raise HTTPException(status_code=401, detail="Not authenticated")

        article = await session.get(Article, article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")

        if article.owner_id != current_user_id and not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Forbidden")

        if body.title is not None:
            article.title = body.title
        if body.content is not None:
            article.content = body.content

        await session.commit()
        await session.refresh(article)

    return article


@handle_errors_async
async def delete_article(article_id: int, request: Request):
    current_user_id = _get_current_user_id(request)

    async with async_session() as session:
        current_user = await session.get(User, current_user_id)
        if not current_user or not current_user.is_active:
            raise HTTPException(status_code=401, detail="Not authenticated")

        article = await session.get(Article, article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")

        if article.owner_id != current_user_id and not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Forbidden")

        await session.delete(article)
        await session.commit()

    return {"message": "Article deleted"}
