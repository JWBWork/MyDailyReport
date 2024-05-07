from os import environ
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from stripe import StripeClient
from src.storage.db import Base, get_async_session
from loguru import logger
from src.routers.users import (User, current_active_user,
                               current_active_verified_user)

stripe_api_key = environ['STRIPE_API_KEY_TEST']
stripe_client = StripeClient(stripe_api_key)

class CheckoutSession(BaseModel):
    session_id: str

subscriptions_router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"]
)

@subscriptions_router.post("/checkout-session")
async def process_checkout_session(
    checkout_session: CheckoutSession,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    logger.info(f"Processing checkout session {checkout_session.session_id=}")
    checkout_session = stripe_client.checkout.sessions.retrieve(checkout_session.session_id)
    subscription_id = checkout_session['subscription']
    user.subscription = subscription_id
    session.add(user)
    await session.commit()
    return {"message": "Subscription updated"}
