from fastapi import APIRouter, Request, Response, HTTPException

from source.schemas.auth import SignUpRequest, SignInRequest
import source.handlers.auth as auth_handler

router = APIRouter()


@router.post("/sign-up")
async def sign_up(body: SignUpRequest, response: Response):
    result = await auth_handler.sign_up(body, response)
    if result is False:
        raise HTTPException(status_code=500, detail="Unexpected error")
    return result


@router.post("/sign-in")
async def sign_in(body: SignInRequest, response: Response):
    result = await auth_handler.sign_in(body, response)
    if result is False:
        raise HTTPException(status_code=500, detail="Unexpected error")
    return result


@router.post("/sign-out")
async def sign_out(response: Response):
    result = await auth_handler.sign_out(response)
    if result is False:
        raise HTTPException(status_code=500, detail="Unexpected error")
    return result


@router.post("/refresh")
async def refresh(request: Request, response: Response):
    result = await auth_handler.refresh(request, response)
    if result is False:
        raise HTTPException(status_code=500, detail="Unexpected error")
    return result
