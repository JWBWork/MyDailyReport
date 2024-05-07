from pathlib import Path
from pprint import pformat

import requests
from config import settings
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from src.routers.integrations.github import github_router
from src.routers.reports import Report, reports_router
from src.routers.users import (User, auth_router, current_active_user,
                               user_router)
from src.routers.subscriptions import subscriptions_router
from src.storage.db import create_db_and_tables
from src.summary.integrations.github.exceptions import (GithubBadRefreshToken,
                                                        GithubException)

env_path = Path().resolve() / '.env'
load_dotenv(env_path)


app = FastAPI(
    debug=True,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(github_router, prefix="/api")
app.include_router(reports_router, prefix="/api")
app.include_router(subscriptions_router, prefix="/api")


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@app.on_event("startup")
async def on_startup():
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables(User, Report)


@app.exception_handler(requests.exceptions.HTTPError)
async def requests_http_error_exception_handler(_: Request, exc: requests.exceptions.HTTPError):
    logger.error(f"HTTP error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": f"{exc}"},
    )


@app.exception_handler(GithubException)
async def github_bad_refresh_token_exception_handler(_: Request, exc: GithubException):
    match exc:
        case GithubBadRefreshToken():
            logger.error(f"Bad refresh token: {exc}")
            return JSONResponse(
                status_code=400,
                content={"message": f"{exc}"},
            )
        case GithubException():
            logger.error(f"Github exception: {exc}")
            return JSONResponse(
                status_code=500,
                content={"message": f"{exc}"},
            )
        case _:
            logger.error(f"Unknown exception: {exc}")
            return JSONResponse(
                status_code=500,
                content={"message": f"Unknown exception {exc}"},
            )

logger.info(pformat(app.routes))
