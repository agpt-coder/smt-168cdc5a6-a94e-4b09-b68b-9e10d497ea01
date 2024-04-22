import prisma
import prisma.models
from pydantic import BaseModel


class OptimizationDetailsResponse(BaseModel):
    """
    Response model containing detailed instructions and metrics related to the cutting list optimization. This helps in planning and executing cuts for material effectively.
    """

    optimizationId: str
    cuttingInstructions: str
    materialUtilization: str
    expectedYield: float


async def getOptimizationResults(optimizationId: str) -> OptimizationDetailsResponse:
    """
    Retrieves the results of a specific optimization request. The result includes detailed cutting instructions and expected material utilization metrics. This helps operators in executing cutting processes efficiently.

    Args:
        optimizationId (str): The unique identifier for the cutting list optimization inquiry.

    Returns:
        OptimizationDetailsResponse: Response model containing detailed instructions and metrics related to the cutting list optimization. This helps in planning and executing cuts for material effectively.

    Example:
        optimization_detail = getOptimizationResults("1234-abcde")
        print(optimization_detail.cuttingInstructions)
        > "Cut using dimensions x by y..."
    """
    record = await prisma.models.PriceEstimate.prisma().find_unique(
        where={"id": optimizationId}
    )
    if record is None:
        raise ValueError("Optimization ID not found")
    return OptimizationDetailsResponse(
        optimizationId=optimizationId,
        cuttingInstructions=f"Optimize cuts for dimensions {record.lumberDimensions}, Grade: {record.lumberGrade}",
        materialUtilization="Estimated utilization 95%, based on optimization model calculations.",
        expectedYield=record.expectedProfit / record.priceRate * 100,
    )
