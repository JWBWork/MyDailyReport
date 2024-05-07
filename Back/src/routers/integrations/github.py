from pprint import pformat
from typing import List

from config import settings
from fastapi import APIRouter, Query, Request, Depends
from loguru import logger
from src.summary.integrations import (
    GithubIntegration, GithubSummary,
    GithubTokenModel, GithubUserModel
)
from src.routers.users import User, current_active_user
from src.routers.reports import Report


github_router = APIRouter(
    prefix="/integrations/github",
    tags=["github", "integrations"]
)

github_integration = GithubIntegration(
    client_id=settings.github_oath_client_id,
    client_secret=settings.github_oath_client_secret
)
github_summary = GithubSummary()

@github_router.get("/")
async def github_auth(code: str):
    logger.info(f"Authorizing {code=}")
    access_token = github_integration.auth(code)
    logger.info(f"Github user: {github_integration.get_user()}")
    return access_token

@github_router.get("/refresh")
async def github_refresh_access_token(refresh_token: str):
    logger.info(f"Refreshing access token for {refresh_token=}")
    return github_integration.refresh_access_token(refresh_token)

@github_router.post("/update")
async def github_update_access_token(token_data: GithubTokenModel):
    logger.info(f"Updating access token for {token_data=}")
    r = github_integration.update_access_token_data(
        **token_data.model_dump()
    )
    logger.info(f"Updated access token for {token_data=}")
    return  r

@github_router.post("/logout")
async def github_signout(user: GithubUserModel):
    logger.info(f"Signing out for {user=}")
    github_integration.signout()

@github_router.get("/user")
async def get_github_repos():
    return github_integration.get_user()

@github_router.get("/repos")
async def get_github_repos():
    return github_integration.get_repos()

@github_router.get("/repos/{repo_name}/commits")
async def get_github_repos(repo_name: str, owner: str):
    response = github_integration.get_repo_commits(
        owner=owner,
        repo_name=repo_name,
    )
    return response

@github_router.get("/report/{owner}/{repo_name}")
async def get_github_summary(
    request: Request, 
    owner: str, 
    repo_name: str, 
    commit_shas: List[str] = Query(None),
    user: User = Depends(current_active_user)
):
    commits = [
        github_integration.get_repo_commit(
            owner=owner,
            repo_name=repo_name,
            sha=sha,
        ) for sha in commit_shas
    ]
    summaries = list()
    for i, commit in enumerate(commits):
        summary = github_summary.summarize_commit_files(commit)
        summaries.extend(summary)
    report_content = "\n\n\n".join(summaries)

    # TODO: see why this results in recursive error
    # report = Report(
    #     name=repo_name,
    #     content="\n\n\n".join(summaries),
    #     user_id=user.id,
    #     user=user
    # )
    
    return {
        # "summary": "\n\n\n".join(summaries),
        "report": {
            "name": repo_name,
            "content": report_content,
        },
        "metadata": {
            "owner": owner,
            "repo_name": repo_name,
            "commit_shas": commit_shas,
        }
    }
