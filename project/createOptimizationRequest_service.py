import uuid
from typing import List, Tuple

import prisma
import prisma.models
from pydantic import BaseModel


class OptimizationResponse(BaseModel):
    """
    Response model with a unique request ID for the optimization and the status of the request.
    """

    requestId: str
    status: str


async def createOptimizationRequest(
    dimensions: List[Tuple[float, float, float]],
    quantities: List[int],
    materialType: str,
    grade: str,
    operatorId: str,
) -> OptimizationResponse:
    """
    Receives customer requirements and initiates the process to optimize cutting patterns. It uses data from the Inventory Tracking Module to ensure material availability and communicates with the Production Recording Module to provide cutting instructions. Expected to return a unique request ID and status.

    Args:
        dimensions (List[Tuple[float, float, float]]): List of dimensions specified by the customer for the cutting process.
        quantities (List[int]): Corresponding quantities for each dimension set specified by the customer.
        materialType (str): Type of material required, as determined by the stock records.
        grade (str): Quality grade of the material required.
        operatorId (str): ID of the operator starting the optimization process. Used for tracking and permissions.

    Returns:
        OptimizationResponse: Response model with a unique request ID for the optimization and the status of the request.

    """
    request_id = uuid.uuid4().hex
    raw_materials = await prisma.models.RawMaterial.prisma().find_many(
        where={"type": materialType, "quantity": {"gte": sum(quantities)}}
    )
    if not raw_materials:
        return OptimizationResponse(
            requestId=request_id, status="Failed: Insufficient Material"
        )
    for dimension, quantity in zip(dimensions, quantities):
        await prisma.models.ProductionRecord.prisma().create(
            data={
                "userId": operatorId,
                "quantityProduced": quantity,
                "RawMaterial": {"connect": {"id": raw_materials[0].id}},
                "FinishedProduct": {
                    "create": {
                        "type": materialType,
                        "quantity": quantity,
                        "unit": "unit",
                        "grade": grade,
                    }
                },
            }
        )
    return OptimizationResponse(requestId=request_id, status="Optimization Successful")
