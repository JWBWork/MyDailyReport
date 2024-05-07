import os
import uuid
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, schemas
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users.db import (SQLAlchemyBaseOAuthAccountTableUUID,
                              SQLAlchemyBaseUserTableUUID,
                              SQLAlchemyUserDatabase)
from fastapi_users.jwt import generate_jwt
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase, SQLAlchemyBaseAccessTokenTableUUID)
from httpx_oauth.clients.google import GoogleOAuth2
from loguru import logger
from sqlalchemy import Column, Date, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from src.email import send_email
from src.storage.db import Base, get_async_session

load_dotenv()

# TODO: separate user functionality to file outside of routing?

SECRET = "SECRET"


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    oauth_accounts: List[OAuthAccount] = relationship(
        "OAuthAccount", lazy="joined")
    reports = relationship("Report", back_populates="user", lazy="joined")
    subscription = Column(String, nullable=True)

    reports_generated_today = Column(Date, nullable=True)
    last_report_date = Column(Date, nullable=True)


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    pass


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user} has registered.")
        token_data = {
            "user_id": str(user.id),
            "email": user.email,
            "aud": self.verification_token_audience,
        }
        token = generate_jwt(
            token_data, self.verification_token_secret, self.verification_token_lifetime_seconds
        )
        email_response = send_email("MyDailyReport Verification", user.email, token)
        logger.info(f"Email sent to {user.email=} with {email_response=}")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)


async def get_access_token_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


google_oauth_client = GoogleOAuth2(
    os.environ["GOOGLE_CLIENT_ID"],
    os.environ["GOOGLE_CLIENT_SECRET"],
)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
current_active_verified_user = fastapi_users.current_user(
    active=True, verified=True)


auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)
auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
    tags=["auth"]
)
auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    tags=["auth"],
)
auth_router.include_router(
    fastapi_users.get_reset_password_router(),
    tags=["auth"],
)
auth_router.include_router(
    fastapi_users.get_verify_router(UserRead),
    tags=["auth"],
)
auth_router.include_router(
    fastapi_users.get_oauth_router(google_oauth_client, auth_backend, SECRET),
    prefix="/google",
    tags=["auth", "google"],
)

user_router = APIRouter(
    prefix="/user",
    tags=["user"]
)
user_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    tags=["users"],
)
