from datetime import datetime
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class GetPriceEstimatesRequest(BaseModel):
    """
    Request parameters for fetching all price estimates. This model is straightforward since it does not require any input parameters.
    """

    pass


class PriceEstimate(BaseModel):
    """
    Details of the price estimate per lumber requirements.
    """

    id: str
    lumber_dimensions: object
    lumber_grade: str
    quantity: int
    price_rate: float
    createdAt: datetime
    updatedAt: datetime
    expected_profit: float


class GetPriceEstimatesResponse(BaseModel):
    """
    Provides a comprehensive list of all price estimates stored in the database, each containing details necessary for review.
    """

    price_estimates: List[PriceEstimate]


async def getPriceEstimates(
    request: GetPriceEstimatesRequest,
) -> GetPriceEstimatesResponse:
    """
    Retrieves a list of all price estimates previously calculated and stored. Useful for reviewing past quotes and prices.

    Args:
        request (GetPriceEstimatesRequest): Request parameters for fetching all price estimates. This model is straightforward since it does not require any input parameters.

    Returns:
        GetPriceEstimatesResponse: Provides a comprehensive list of all price estimates stored in the database, each containing details necessary for review.

    Example:
        request = GetPriceEstimatesRequest()
        response = await getPriceEstimates(request)
        > GetPriceEstimatesResponse(price_estimates=[prisma.models.PriceEstimate(id='1', ...)])
    """
    price_estimates = await prisma.models.PriceEstimate.prisma().find_many()
    return GetPriceEstimatesResponse(price_estimates=price_estimates)
