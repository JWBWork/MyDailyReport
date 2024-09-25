import timeit
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, fields
from enum import StrEnum
from pathlib import Path
from typing import Optional, List

import openai
import requests
from config import settings
from loguru import logger
from pydantic import BaseModel
from src.summary.integrations.github.exceptions import (GithubBadRefreshToken,
                                                        GithubException)
from src.summary.integrations.integration import Integration
from src.summary.integrations.token_cost import estimate_token_cost
from src.summary.summary import Summary

FILTERED_EXTENSIONS = (
    ".csv", ".xlsx", ".png", ".pdf", ".docx", ".doc",".svg", ".gltf", ".gltf.import", ".sqlite", ".suo", ".exe"
)

@dataclass
class CommitAuthor:
    name: str
    email: str
    date: str


@dataclass
class CommitFile:
    sha: str
    filename: str
    status: str
    additions: int
    deletions: int
    changes: int
    blob_url: str
    raw_url: str
    contents_url: str
    token_cost: Optional[int] = None
    patch: Optional[str] = None

    @classmethod
    def from_json(cls, json):
        class_fields = {field.name for field in fields(cls)}
        json['token_cost'] = estimate_token_cost(
            json['status'], json['filename'], json.get('patch')
        )
        return cls(**{k: v for k, v in json.items() if k in class_fields})

    def json(self):
        return self.__dict__


@dataclass
class Commit:
    sha: str
    url: str
    html_url: str
    message: str
    # status: str
    token_cost: Optional[int] = None
    files: Optional[list[CommitFile]] = None
    author: Optional[CommitAuthor] = None

    @classmethod
    def from_json(cls, json):
        class_fields = {field.name for field in fields(cls)}
        _kwargs = {k: v for k, v in json.items() if k in class_fields}
        _kwargs = {
            **_kwargs,
            **{k: v for k, v in json["commit"].items() if k in class_fields},
        }
        if _kwargs.get("files"):
            _kwargs["files"] = [
                CommitFile.from_json(file) for file in _kwargs["files"]
                if not any(file.get("filename", '').lower().endswith(ext) for ext in FILTERED_EXTENSIONS)
            ]
        if _kwargs.get("author"):
            _kwargs["author"] = CommitAuthor(**_kwargs["author"])
        _kwargs['token_cost'] = estimate_token_cost(
            _kwargs['message'], _kwargs['author'].name, _kwargs['author'].email
        ) + sum(file.token_cost for file in _kwargs.get("files", []))
        _commit = cls(
            **{k: v for k, v in _kwargs.items() if k in class_fields})
        return _commit

    def json(self):
        return self.__dict__


@dataclass
class Repo:
    id: int
    node_id: str
    name: str
    full_name: str
    private: bool
    owner: dict
    html_url: str
    description: str
    fork: bool
    url: str
    created_at: str
    updated_at: str
    pushed_at: str
    size: int
    stargazers_count: int
    watchers_count: int
    forks_count: int
    open_issues_count: int
    default_branch: str
    homepage: Optional[str] = None
    language: Optional[str] = None
    commits: Optional[list[Commit]] = None

    def __post_init__(self):
        if self.commits:
            self.commits = [Commit(**commit) for commit in self.commits]

    @classmethod
    def from_json(cls, json):
        class_fields = {field.name for field in fields(cls)}
        return cls(**{k: v for k, v in json.items() if k in class_fields})

    def json(self):
        return self.__dict__


class GithubUserModel(BaseModel):
    login: str


class CommitAuthorModel(BaseModel):
    name: str
    email: str
    date: str


class CommitFileModel(BaseModel):
    additions: int
    changes: int
    deletions: int
    filename: str
    patch: str
    raw_url: str
    selected: bool
    status: str
    token_cost: int


class GithubCommitModel(BaseModel):
    additions: Optional[int] = None
    author: CommitAuthorModel
    changes: Optional[int] = None
    deletions: Optional[int] = None
    filename: Optional[str] = None
    files: List[CommitFileModel]
    message: str
    patch: Optional[str] = None
    raw_url: Optional[str] = None
    sha: str
    status: Optional[str] = None
    token_cost: int


class GithubTokenModel(BaseModel):
    access_token: Optional[str] = None
    expires_in: Optional[int] = None
    refresh_token: Optional[str] = None
    refresh_token_expires_in: Optional[int] = None
    scope: Optional[str] = None
    token_type: Optional[str] = None
    timestamp: Optional[int] = None


class GithubIntegration(Integration):
    def __init__(self, client_id, client_secret):
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.access_token: str = None
        self.expires_in: int
        self.refresh_token: str
        self.refresh_token_expires_in: int
        self.scope: str
        self.token_type: str
        self.api_url: str = "https://api.github.com"

    def get(self, path, **kwargs):
        headers = kwargs.get("headers")
        if headers is None and self.access_token is not None:
            kwargs["headers"] = {
                'Authorization': f'Bearer {self.access_token}'}
        response = requests.get(f"{self.api_url}/{path}", **kwargs)
        # TODO: decorator for requests.exceptions.HTTPError: 401 Client Error: Unauthorized for url: ht
        response.raise_for_status()
        return response

    def post(self, path, data=None, json=None, **kwargs):
        kwargs["headers"] = kwargs.get("headers") or {
            'Authorization': f'Bearer {self.access_token}'}
        response = requests.post(
            f"{self.api_url}/{path}", data=data, json=json, **kwargs)
        response.raise_for_status()
        return response

    def update_access_token_data(self, **data):
        self.access_token = data["access_token"]
        self.expires_in = data["expires_in"]
        self.refresh_token = data["refresh_token"]
        self.refresh_token_expires_in = data["refresh_token_expires_in"]
        self.token_type = data["token_type"]
        self.scope = data["scope"]

    def auth(self, code):
        response = requests.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code
            },
            headers={
                "Accept": "application/json"
            }
        )
        response.raise_for_status()
        data = response.json()
        self.update_access_token_data(**data)
        return data

    def refresh_access_token(self, refresh_token: str = None):
        response = requests.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": refresh_token or self.refresh_token,
                "grant_type": "refresh_token"
            },
            headers={
                "Accept": "application/json"
            }
        )
        response.raise_for_status()
        data = response.json()
        if error := data.get("error"):
            # TODO: move to function w/ case statement?
            if error == "bad_refresh_token":
                raise GithubBadRefreshToken(data["error_description"])
            else:
                raise GithubException(data["error_description"])
        else:
            self.update_access_token_data(**data)
            return response

    def signout(self):
        self.access_token = None
        self.expires_in = None
        self.refresh_token = None
        self.refresh_token_expires_in = None
        self.token_type = None
        self.scope = None

    def get_user(self):
        response = self.get("user")
        return response.json()

    def get_repos(self):
        response = self.get("user/repos")
        repos = [Repo.from_json(repo_json) for repo_json in response.json()]
        return repos

    def get_repo_commits(self, owner: str, repo_name: str, since: str = None, until: str = None):
        repo_commits = self.get(f"repos/{owner}/{repo_name}/commits").json()
        repo_commits = [Commit.from_json(commit) for commit in repo_commits]

        with ThreadPoolExecutor() as executor:
            repo_commits = executor.map(
                self.get_repo_commit,
                *zip(*[(owner, repo_name, commit.sha) for commit in repo_commits])
            )
            executor.shutdown()

        return list(repo_commits)

    def get_repo_commit(self, owner: str, repo_name: str, sha: str):
        response = self.get(f"repos/{owner}/{repo_name}/commits/{sha}")
        return Commit.from_json(response.json())


class GithubSummary(Summary):
    class Templates(StrEnum):
        COMMIT = "git_commit"
        COMMIT_FILE = "git_commit_file"

    def summarize_commit_files(self, commit: GithubCommitModel) -> list[str]:
        _filter_out = (
            ".csv", ".xlsx", ".png", ".pdf", ".docx", ".doc",
            ".svg", ".gltf", ".gltf.import", ".sqlite", ".suo"
        )
        files_to_summarize = [
            file for file in commit.files
            if not any(
                file.filename.lower().endswith(ext)
                for ext in _filter_out
            )
            if file.selected
        ]

        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(
                    self.get_summary,
                    self.Templates.COMMIT_FILE,
                    message=commit.message,
                    status=file.status,
                    filename=file.filename,
                    patch=file.patch,
                ) for file in files_to_summarize
            ]
            summaries = [future.result() for future in futures]
        return list(summaries)
