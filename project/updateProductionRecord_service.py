import prisma
import prisma.models
from pydantic import BaseModel


class UpdateProductionRecordResponse(BaseModel):
    """
    Response model for updating a production record. Will return the updated details of the production record.
    """

    recordId: str
    rawMaterialType: str
    finishedProductType: str
    quantityProduced: int
    newDimensions: str
    newGrade: str


async def updateProductionRecord(
    recordId: str,
    rawMaterialId: str,
    finishedProductId: str,
    quantityProduced: int,
    newDimensions: str,
    newGrade: str,
) -> UpdateProductionRecordResponse:
    """
    Updates an existing production record's details. This is useful for corrections or adjustments in data logs.

    Args:
        recordId (str): The unique identifier of the production record to be updated.
        rawMaterialId (str): The raw material identifier used in this production record.
        finishedProductId (str): The finished product identifier after processing the raw material.
        quantityProduced (int): The updated quantity of the finished product produced during the production process.
        newDimensions (str): Updated dimensions for the produced lumber, if applicable.
        newGrade (str): New quality grade of the finished product if there are changes to report.

    Returns:
        UpdateProductionRecordResponse: Response model for updating a production record. Will return the updated details of the production record.
    """
    record = await prisma.models.ProductionRecord.prisma().find_unique(
        where={"id": recordId}
    )
    if record is None:
        raise ValueError("prisma.models.ProductionRecord not found")
    await prisma.models.ProductionRecord.prisma().update(
        where={"id": recordId},
        data={
            "rawMaterialId": rawMaterialId,
            "finishedProductId": finishedProductId,
            "quantityProduced": quantityProduced,
            "RawMaterial": {"update": {"type": newDimensions}},
            "FinishedProduct": {"update": {"grade": newGrade, "type": newDimensions}},
        },
    )
    updated_record = await prisma.models.ProductionRecord.prisma().find_unique(
        where={"id": recordId}, include={"RawMaterial": True, "FinishedProduct": True}
    )
    response = UpdateProductionRecordResponse(
        recordId=recordId,
        rawMaterialType=updated_record.RawMaterial.type,
        finishedProductType=updated_record.FinishedProduct.type,
        quantityProduced=quantityProduced,
        newDimensions=newDimensions,
        newGrade=newGrade,
    )
    return response
