from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class ProductionRecordResponse(BaseModel):
    """
    Response model containing detailed information about a single production record.
    """

    finishedProductId: str
    id: str
    userId: str
    rawMaterialId: str
    quantityProduced: int
    createdAt: datetime
    updatedAt: datetime


async def getProductionRecord(recordId: str) -> ProductionRecordResponse:
    """
    Fetches a specific production record by its ID. This is useful for detailed examination of a single production event.

    Args:
        recordId (str): The unique identifier for the production record to be retrieved.

    Returns:
        ProductionRecordResponse: Response model containing detailed information about a single production record.

    Example:
        record = await getProductionRecord('123e4567-e89b-12d3-a456-426614174000')
        print(record)
        > ProductionRecordResponse(finishedProductId='002a4567-e89b-12d3-a456-426614174999',
                                   id='123e4567-e89b-12d3-a456-426614174000',
                                   userId='200e4567-e89b-12d3-a456-426614174550',
                                   rawMaterialId='300t4578-e89g-13c3-b567-416614274010',
                                   quantityProduced=150,
                                   createdAt=datetime(2023, 1, 20, 14, 50),
                                   updatedAt=datetime(2023, 2, 20, 12, 30))
    """
    record = await prisma.models.ProductionRecord.prisma().find_unique(
        where={"id": recordId},
        include={"User": True, "RawMaterial": True, "FinishedProduct": True},
    )
    if record is None:
        raise ValueError("No production record found with the given ID.")
    response = ProductionRecordResponse(
        finishedProductId=record.FinishedProduct.id,
        id=record.id,
        userId=record.User.id,
        rawMaterialId=record.RawMaterial.id,
        quantityProduced=record.quantityProduced,
        createdAt=record.createdAt,
        updatedAt=record.updatedAt,
    )
    return response
