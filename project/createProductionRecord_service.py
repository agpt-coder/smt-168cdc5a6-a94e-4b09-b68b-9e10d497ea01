from typing import Dict

import prisma
import prisma.models
from pydantic import BaseModel


class CreateProductionRecordResponse(BaseModel):
    """
    Defines the structure of the response for the newly created production record which includes a reference ID and a confirmation message globally used to guide further actions.
    """

    confirmationMessage: str
    recordId: str


async def createProductionRecord(
    userId: str,
    rawMaterialId: str,
    finishedProductId: str,
    quantityProduced: int,
    lumberDimensions: Dict[str, float],
    lumberGrade: str,
) -> CreateProductionRecordResponse:
    """
    Creates a new production record for daily outputs. It captures quantities, dimensions, and grades of lumber produced. This is crucial for tracking and planning purposes.

    Args:
    userId (str): ID of the user who is logging this production record.
    rawMaterialId (str): ID of the raw material used for this production batch.
    finishedProductId (str): ID for the finished product entry linked to this production record.
    quantityProduced (int): Quantity of the finished product produced in this production run.
    lumberDimensions (Dict[str, float]): Physical dimensions of the lumber produced defined in length, width, thickness.
    lumberGrade (str): Grade classification of the produced lumber based on quality.

    Returns:
    CreateProductionRecordResponse: Defines the structure of the response for the newly created production record which includes a reference ID and a confirmation message globally used to guide further actions.

    Example:
        createProductionRecord("user_uuid", "raw_mat_uuid", "finished_prod_uuid", 100, {"length": 2.5, "width": 0.5, "thickness": 0.05}, "A")
        > {"confirmationMessage": "Production record created successfully!", "recordId": "new_record_uuid"}
    """
    new_record = await prisma.models.ProductionRecord.prisma().create(
        data={
            "userId": userId,
            "rawMaterialId": rawMaterialId,
            "finishedProductId": finishedProductId,
            "quantityProduced": quantityProduced,
            "lumberDimensions": lumberDimensions,
            "lumberGrade": lumberGrade,
        }
    )
    return CreateProductionRecordResponse(
        confirmationMessage="Production record created successfully!",
        recordId=new_record.id,
    )
