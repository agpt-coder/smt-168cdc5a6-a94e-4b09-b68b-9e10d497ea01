import prisma
import prisma.models
from pydantic import BaseModel


class PriceEstimateResponse(BaseModel):
    """
    Provides the calculated price and generated quote id for the requested lumber items.
    """

    estimatedPrice: float
    quoteId: str


async def createPriceEstimate(
    dimensions: str, grade: str, quantity: int
) -> PriceEstimateResponse:
    """
    This endpoint accepts dimensions, grade, and quantity of lumber from the user, calculates the price using predefined rates fetched from the Inventory Tracking Module, and generates a quote. The quote is then stored and can be used by the Sales and Invoicing Module.

    Args:
        dimensions (str): Lumber dimensions in the form of width x height x length (e.g., 2x4x8).
        grade (str): The grade of the lumber, determining quality and price scaling.
        quantity (int): The number of specified lumber items the customer wants to price.

    Returns:
        PriceEstimateResponse: Provides the calculated price and generated quote id for the requested lumber items.
    """
    predefined_rate = await prisma.models.PriceEstimate.prisma().find_many(
        where={"lumberDimensions": dimensions, "lumberGrade": grade}, take=1
    )
    if not predefined_rate:
        raise ValueError("No predefined rate available for these specifications.")
    price_rate = predefined_rate[0].priceRate
    total_price = price_rate * quantity
    created_quote = await prisma.models.Quote.prisma().create(
        data={
            "priceEstimate": {
                "create": {
                    "lumberDimensions": dimensions,
                    "lumberGrade": grade,
                    "quantity": quantity,
                    "priceRate": price_rate,
                }
            }
        },
        include={"priceEstimate": True},
    )
    quote_id = created_quote.id
    return PriceEstimateResponse(estimatedPrice=total_price, quoteId=quote_id)
