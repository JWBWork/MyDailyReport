from os import environ
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
import stripe
from src.storage.db import Base, get_async_session
from loguru import logger
from src.routers.users import (User, current_active_user,
                               current_active_verified_user, user_router)

stripe.api_key = environ['STRIPE_API_KEY_TEST']

class TokenPurchaseRequest(BaseModel):
    quantity: int

class CheckoutSession(BaseModel):
    session_id: str

tokens_router = APIRouter(
    prefix="/tokens",
    tags=["tokens"]
)

@tokens_router.get("/")
async def get_tokens(user: User = Depends(current_active_user)):
    return {"tokens": user.tokens}

@tokens_router.post("/begin-checkout")
async def process_checkout_session(
    checkout_session: TokenPurchaseRequest,
    user: User = Depends(current_active_user),
):
    checkout_session = stripe.checkout.Session.create(
        success_url="https://localhost:9000/user?checkout-session-id={CHECKOUT_SESSION_ID}",
        line_items=[{
            "price": "price_1PEw6tA8jMGv8c7Qb6RjwohV",
            "quantity": checkout_session.quantity,
            "adjustable_quantity": {
                "enabled": True, 
                "minimum": 10,
                "maximum": 1000
            },
        }],
        customer_email= user.email,
        automatic_tax={"enabled": True},
        mode="payment"
    )
    return {
        "stripe_url": checkout_session.url
    }

@tokens_router.post("/process-checkout")
async def process_checkout(
    checkout_session: CheckoutSession,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    checkout_session = stripe.checkout.Session.retrieve(checkout_session.session_id)
    line_items = checkout_session.list_line_items()
    quantity = line_items.data[0].quantity
    if checkout_session.payment_status == "paid":
        user.tokens += quantity
        session.add(user)
        await session.commit()
        return {"message": "Payment successful"}
    else:
        return {"message": "Payment failed"}
