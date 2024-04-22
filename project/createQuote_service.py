from datetime import datetime
from typing import Dict

import prisma
import prisma.models
from pydantic import BaseModel


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


class QuoteResponse(BaseModel):
    """
    Response model representing the generated customer quote.
    """

    quoteId: str
    createdAt: datetime
    priceEstimateDetails: PriceEstimate


async def createQuote(
    customerContactId: str,
    lumberDimensions: Dict[str, float],
    lumberGrade: str,
    quantity: int,
) -> QuoteResponse:
    """
    Creates a new customer quote based on lumber dimensions, grade, and quantity.
    This endpoint uses predefined rates to calculate prices and returns a generated quote.

    Args:
        customerContactId (str): The unique identifier for the customer to whom the quote is being issued.
        lumberDimensions (Dict[str, float]): The dimensions of the lumber for which the price is being estimated, expressed in JSON format.
        lumberGrade (str): The grade of the lumber for the quotation.
        quantity (int): The quantity of lumber required for the quote.

    Returns:
        QuoteResponse: Response model representing the generated customer quote.

    Example:
        await createQuote(
            "e1c1c92a-9da3-467d-ae0f-52ac1c442b57",
            {"length": 2.0, "width": 4.0, "height": 8.0},
            "High",
            100
        )
    """
    price_rate_per_unit = 2.5
    expected_profit = quantity * price_rate_per_unit * 0.2
    price_estimate = await prisma.models.PriceEstimate.prisma().create(
        {
            "lumberDimensions": lumberDimensions,
            "lumberGrade": lumberGrade,
            "quantity": quantity,
            "priceRate": price_rate_per_unit,
            "expectedProfit": expected_profit,
            "createdAt": datetime.now(),
            "updatedAt": datetime.now(),
        }
    )
    quote = await prisma.models.Quote.prisma().create(
        {
            "customerContactId": customerContactId,
            "createdAt": datetime.now(),
            "updatedAt": datetime.now(),
            "priceEstimate": {"connect": {"id": price_estimate.id}},
        }
    )
    return QuoteResponse(
        quoteId=quote.id,
        createdAt=quote.createdAt,
        priceEstimateDetails=PriceEstimate(
            id=price_estimate.id,
            lumber_dimensions=lumberDimensions,
            lumber_grade=lumberGrade,
            quantity=quantity,
            price_rate=price_rate_per_unit,
            createdAt=price_estimate.createdAt,
            updatedAt=price_estimate.updatedAt,
            expected_profit=expected_profit,
        ),
    )
