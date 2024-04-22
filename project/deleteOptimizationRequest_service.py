import prisma
import prisma.models
from pydantic import BaseModel


class DeleteOptimizationResponse(BaseModel):
    """
    Response model for the deletion of an optimization. It will indicate whether the deletion was successful or if there was an error.
    """

    success: bool
    message: str


async def deleteOptimizationRequest(optimizationId: str) -> DeleteOptimizationResponse:
    """
    Allows for deletion of a specific optimization request. This might be necessary in cases where an optimization becomes irrelevant due to changing customer requirements or inventory changes.

    Args:
    optimizationId (str): The unique identifier for the optimization entry that needs to be deleted.

    Returns:
    DeleteOptimizationResponse: Response model for the deletion of an optimization. It will indicate whether the deletion was successful or if there was an error.
    """
    try:
        optimization = await prisma.models.PriceEstimate.prisma().find_unique(
            where={"id": optimizationId}
        )
        if optimization is None:
            return DeleteOptimizationResponse(
                success=False, message="Optimization request not found."
            )
        await prisma.models.PriceEstimate.prisma().delete(where={"id": optimizationId})
        return DeleteOptimizationResponse(
            success=True, message="Optimization request deleted successfully."
        )
    except Exception as e:
        return DeleteOptimizationResponse(
            success=False, message=f"An error occurred during deletion: {str(e)}"
        )
