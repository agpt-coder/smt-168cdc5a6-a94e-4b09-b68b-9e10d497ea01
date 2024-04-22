from datetime import datetime
from typing import Any, Dict

import prisma
import prisma.models
from pydantic import BaseModel


class GetPriceEstimateResponse(BaseModel):
    """
    Response model representing detailed information about a specific price estimate.
    """

    id: str
    lumberDimensions: Dict[str, Any]
    lumberGrade: str
    quantity: int
    priceRate: float
    createdAt: datetime
    updatedAt: datetime
    expectedProfit: float


async def getPriceEstimate(estimateId: str) -> GetPriceEstimateResponse:
    """
    Retrieves detailed information for a specific price estimate by ID. Allows users to view the calculated details and quoted price of a specific estimate.

    Args:
        estimateId (str): Unique identifier for the price estimate.

    Returns:
        GetPriceEstimateResponse: Response model representing detailed information about a specific price estimate.
    """
    estimate = await prisma.models.PriceEstimate.prisma().find_unique(
        where={"id": estimateId}
    )
    if estimate is None:
        raise ValueError("Price estimate with the provided ID does not exist.")
    return GetPriceEstimateResponse(
        id=estimate.id,
        lumberDimensions=estimate.lumberDimensions,
        lumberGrade=estimate.lumberGrade,
        quantity=estimate.quantity,
        priceRate=estimate.priceRate,
        createdAt=estimate.createdAt,
        updatedAt=estimate.updatedAt,
        expectedProfit=estimate.expectedProfit,
    )
