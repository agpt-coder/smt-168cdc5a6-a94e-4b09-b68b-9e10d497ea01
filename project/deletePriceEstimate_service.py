import prisma
import prisma.models
from pydantic import BaseModel


class DeletePriceEstimateResponse(BaseModel):
    """
    This model indicates success of the price estimate deletion. No actual data about the deleted estimate is returned to conform with deletion operation principles where the response usually just confirms the completion of the operation.
    """

    success: bool


async def deletePriceEstimate(estimateId: str) -> DeletePriceEstimateResponse:
    """
    Deletes a specific price estimate from the system permanently. Useful for cleaning up outdated or erroneous quotes.

    Args:
        estimateId (str): The unique identifier of the price estimate to delete.

    Returns:
        DeletePriceEstimateResponse: This model indicates success of the price estimate deletion. No actual data about the deleted estimate is returned to conform with deletion operation principles where the response usually just confirms the completion of the operation.

    Example:
        estimateId = 'some-unique-identifier-for-a-price-estimate'
        response = deletePriceEstimate(estimateId)
        > DeletePriceEstimateResponse(success=True)
    """
    delete_count = await prisma.models.PriceEstimate.prisma().delete_many(
        where={"id": estimateId}
    )
    return DeletePriceEstimateResponse(success=delete_count > 0)
