from typing import Dict

import prisma
import prisma.models
from pydantic import BaseModel


class UpdatePriceEstimateResponse(BaseModel):
    """
    The updated price estimate entry reflecting new dimensions, grades, and recalculated price.
    """

    estimateId: str
    lumberDimensions: Dict[str, float]
    lumberGrade: str
    quantity: int
    newPrice: float
    quoteId: str


async def updatePriceEstimate(
    estimateId: str, lumberDimensions: Dict[str, float], lumberGrade: str, quantity: int
) -> UpdatePriceEstimateResponse:
    """
    Updates an existing price estimate. This may involve changes to dimensions, grades, or quantities, which would then trigger a re-calculation of the price based on current rates from the Inventory Tracking Module.

    Args:
        estimateId (str): The unique identifier of the price estimate to be updated.
        lumberDimensions (Dict[str, float]): New lumber dimensions in a structured format such as {length:, width:, height:}.
        lumberGrade (str): New grade of the lumber which affects price calculations.
        quantity (int): New quantity of the lumber required for recalculating total price.

    Returns:
        UpdatePriceEstimateResponse: The updated price estimate entry reflecting new dimensions, grades, and recalculated price.
    """
    price_estimate = await prisma.models.PriceEstimate.prisma().find_unique(
        where={"id": estimateId}
    )
    if price_estimate is None:
        raise ValueError("The specified Price Estimate does not exist.")
    new_price = calculateNewPriceRate(lumberDimensions, lumberGrade) * quantity
    await prisma.models.PriceEstimate.prisma().update(
        where={"id": estimateId},
        data={
            "lumberDimensions": lumberDimensions,
            "lumberGrade": lumberGrade,
            "quantity": quantity,
            "priceRate": new_price / quantity,
        },
    )
    quote_id = price_estimate.quoteId if price_estimate.quoteId else ""
    return UpdatePriceEstimateResponse(
        estimateId=estimateId,
        lumberDimensions=lumberDimensions,
        lumberGrade=lumberGrade,
        quantity=quantity,
        newPrice=new_price,
        quoteId=quote_id,
    )


def calculateNewPriceRate(
    lumberDimensions: Dict[str, float], lumberGrade: str
) -> float:
    """
    Simulates price calculation based on lumber dimensions and grade.
    This is a placeholder function, assuming prices are influenced by volume and quality grade.

    Args:
        lumberDimensions (Dict[str, float]): The dimensions of the lumber.
        lumberGrade (str): The grade of the lumber.

    Returns:
        float: Calculated price based on dimensions and lumber grade.
    """
    length = lumberDimensions.get("length", 1)
    width = lumberDimensions.get("width", 1)
    height = lumberDimensions.get("height", 1)
    base_price = 50.0
    grade_multiplier = 1.1 if lumberGrade == "A" else 1.0 if lumberGrade == "B" else 0.9
    return base_price * (length * width * height) * grade_multiplier
