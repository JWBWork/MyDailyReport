from datetime import datetime
import requests

from typing import List, Dict, Annotated
from config import settings
from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
from fastapi.datastructures import QueryParams
from fastapi.middleware.cors import CORSMiddleware
from src.integrations import GithubIntegration, GithubSummary, GithubTokenModel
from src.integrations.github.exceptions import GithubException, GithubBadRefreshToken
from pprint import pformat

from loguru import logger

app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

github_integration = GithubIntegration(
    client_id=settings.github_oath_client_id,
    client_secret=settings.github_oath_client_secret
)
github_summary = GithubSummary()

@app.get("/authorize/github")
async def github_auth(code: str):
    access_token = github_integration.auth(code)
    # user = github_integration.get("user").json()
    logger.info(f"User: {github_integration.get_user()}")
    return access_token

@app.get("/authorize/github/refresh")
async def github_refresh_access_token(refresh_token: str):
    logger.info(f"Refreshing access token for {refresh_token=}")
    return github_integration.refresh_access_token(refresh_token)

@app.post("/authorize/github/update")
async def github_update_access_token(token_data: GithubTokenModel):
    logger.info(f"Updating access token for {token_data=}")
    return github_integration.update_access_token_data(**token_data.model_dump())


@app.get("/summary/github/user")
async def get_github_repos():
    return github_integration.get_user()

@app.get("/summary/github/repos")
async def get_github_repos():
    return github_integration.get_repos()

@app.get("/summary/github/repos/{repo_name}/commits")
async def get_github_repos(repo_name: str, owner: str):
    response = github_integration.get_repo_commits(
        owner=owner,
        repo_name=repo_name,
    )
    return response

@app.get("/summary/github/{owner}/{repo_name}")
async def get_github_summary(request: Request, owner: str, repo_name: str, commit_shas: List[str] = Query(None)):
    commits = [
        github_integration.get_repo_commit(
            owner=owner,
            repo_name=repo_name,
            sha=sha,
        ) for sha in commit_shas
    ]
    summaries = list()
    for i, commit in enumerate(commits):
        logger.info(f"Generating summary for {i}/{len(commits)}")
        summary = github_summary.summarize_commit_files(commit)
        summaries.extend(summary)
    logger.info(f"Summaries:\n\n{pformat(summaries)}")
    
    return {
        "summary": "\n\n\n".join(summaries),
        "metadata": {
            "owner": owner,
            "repo_name": repo_name,
            "commit_shas": commit_shas,
        }
    }

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