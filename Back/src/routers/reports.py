from fastapi import APIRouter, Depends, Request, HTTPException
from loguru import logger
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy_utils import UUIDType
# from sqlalchemy.dialects.postgresql import UUID
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.routers.users import (User, current_active_user,
                               current_active_verified_user)
from src.storage.db import Base, get_async_session


class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    content = Column(String, nullable=False)

    user_id = Column(UUIDType(binary=False), ForeignKey(User.id), nullable=False)
    user = relationship("User", back_populates="reports", lazy="joined")

class ReportModel(BaseModel):
    name: str
    content: str

reports_router = APIRouter(
    prefix="/reports",
    tags=["reports"]
)

@reports_router.post("/")
async def save_report(
    report: ReportModel, 
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    # TODO: Save report to database
    logger.info(f"Saving report {report.name=}, {report.content=}")
    existing_report_query = await session.execute(select(Report).where(Report.name == report.name))
    existing_report = existing_report_query.scalars().first()
    if existing_report:
        existing_report.content = report.content
        session.add(existing_report)
        await session.commit()
        logger.info(f"Updated report {existing_report=}")
        return {"message": "Updated report"}
    else:
        new_report = Report(
            name=report.name,
            content=report.content,
            user_id=user.id,
            user=user
        )
        session.add(new_report)
        await session.commit()
        logger.info(f"{user.reports=}")
        return {"message": "Create report"}

@reports_router.get("/")
async def get_reports(
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    user_reports_query = await session.execute(select(Report).where(Report.user_id == user.id))
    user_reports = user_reports_query.unique().scalars().all()
    # TODO: filter user id out of response?
    return {
        "reports": user_reports
    }
