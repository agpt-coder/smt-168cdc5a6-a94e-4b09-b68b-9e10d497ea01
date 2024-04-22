from datetime import datetime
from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class OptimizationRecord(BaseModel):
    """
    Detailed record of an optimization request including related user and production data.
    """

    id: str
    date_created: datetime
    created_by: prisma.models.User
    details: str


class GetOptimizationsResponse(BaseModel):
    """
    This response model provides a list of cutting optimization requests along with pagination metadata.
    """

    optimizations: List[OptimizationRecord]
    total_records: int
    current_page: int
    total_pages: int


class User(BaseModel):
    id: str
    email: str


async def listOptimizations(
    page: int,
    limit: int,
    start_date: Optional[datetime],
    end_date: Optional[datetime],
    user_id: Optional[str],
) -> GetOptimizationsResponse:
    """
    Lists all cutting optimization requests. This can be used by operators to review past optimizations and by management for auditing and planning purposes.

    Args:
        page (int): Specifies the page number of the results to retrieve.
        limit (int): Specifies the number of results per page.
        start_date (Optional[datetime]): Optional parameter to filter records that were created after a specific date.
        end_date (Optional[datetime]): Optional parameter to filter records that were created before a specific date.
        user_id (Optional[str]): Optional parameter to filter records by a specific user's ID.

    Returns:
        GetOptimizationsResponse: This response model provides a list of cutting optimization requests along with pagination metadata.
    """
    query_conditions = []
    if start_date:
        query_conditions.append({"createdAt": {"gte": start_date}})
    if end_date:
        query_conditions.append({"createdAt": {"lte": end_date}})
    if user_id:
        query_conditions.append({"userId": user_id})
    total_optimizations = await prisma.models.ProductionRecord.prisma().count(
        where={"AND": query_conditions}
    )
    production_records = await prisma.models.ProductionRecord.prisma().find_many(
        where={"AND": query_conditions},
        skip=(page - 1) * limit,
        take=limit,
        include={"prisma.models.User": True},
    )
    total_pages = (total_optimizations + limit - 1) // limit
    optimizations = [
        OptimizationRecord(
            id=rec.id,
            date_created=rec.createdAt,
            created_by=rec.User,
            details="Details of production",
        )
        for rec in production_records
    ]
    response = GetOptimizationsResponse(
        optimizations=optimizations,
        total_records=total_optimizations,
        current_page=page,
        total_pages=total_pages,
    )
    return response
