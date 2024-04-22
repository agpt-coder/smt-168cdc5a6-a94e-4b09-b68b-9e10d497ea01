from datetime import datetime
from typing import List

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


class Quote(BaseModel):
    """
    Details of quotes associated with the customer.
    """

    id: str
    priceEstimate: List[PriceEstimate]


class GetQuoteDetailsResponse(BaseModel):
    """
    Response model returning the detailed information of a specific quote. Includes connected customer contact details for comprehensive tracking and follow-up.
    """

    quote: Quote


class QuoteDetails(BaseModel):
    """
    Schema for quote details including associated price estimates to send as a response.
    """

    id: str
    priceEstimate: List[PriceEstimate]


async def getQuote(quoteId: str) -> GetQuoteDetailsResponse:
    """
    Retrieves details of a specific quote using its ID. This allows sales managers and system administrators to review, manage, and follow up on quotes issued to customers.

    Args:
        quoteId (str): The unique identifier for the quote to be retrieved. This is included in the URL as a path parameter.

    Returns:
        GetQuoteDetailsResponse: Response model returning the detailed information of a specific quote. Includes connected customer contact details for comprehensive tracking and follow-up.

    Example:
        quoteId = '123e4567-e89b-12d3-a456-426655440000'
        response = await getQuote(quoteId)
        > GetQuoteDetailsResponse(quote=QuoteDetails(id='123e4567-e89b-12d3-a456-426655440000', priceEstimate=[PriceEstimate(...)]))
    """
    quote_record = await prisma.models.Quote.prisma().find_unique(
        where={"id": quoteId}, include={"priceEstimate": True}
    )
    if quote_record is None:
        raise ValueError(f"No quote found with ID {quoteId}")
    response = GetQuoteDetailsResponse(
        quote=QuoteDetails(id=quote_record.id, priceEstimate=quote_record.priceEstimate)
    )
    return response
