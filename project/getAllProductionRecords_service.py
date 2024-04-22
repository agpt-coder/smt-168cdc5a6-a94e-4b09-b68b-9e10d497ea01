from datetime import datetime
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class GetAllProductionRecordsRequest(BaseModel):
    """
    This model represents the request for fetching all production records. It could be augmented with query parameters for filtering and pagination.
    """

    pass


class ProductionRecordDetails(BaseModel):
    """
    Detailed information about each production event.
    """

    id: str
    userId: str
    rawMaterialId: str
    finishedProductId: str
    quantityProduced: int
    createdAt: datetime
    updatedAt: datetime


class GetAllProductionRecordsResponse(BaseModel):
    """
    This model encapsulates the response data for all production records. Each record includes details of the production process such as the product type, quantity, and associated materials.
    """

    records: List[ProductionRecordDetails]


async def getAllProductionRecords(
    request: GetAllProductionRecordsRequest,
) -> GetAllProductionRecordsResponse:
    """
    Retrieves a list of all production records. This includes historical data which is necessary for analysis and reporting.

    Args:
        request (GetAllProductionRecordsRequest): This model represents the request for fetching all production records. It could be augmented with query parameters for filtering and pagination.

    Returns:
        GetAllProductionRecordsResponse: This model encapsulates the response data for all production records. Each record includes details of the production process such as the product type, quantity, and associated materials.
    """
    records = await prisma.models.ProductionRecord.prisma().find_many(
        include={"User": True, "RawMaterial": True, "FinishedProduct": True}
    )
    response_records = [
        ProductionRecordDetails(
            id=record.id,
            userId=record.userId,
            rawMaterialId=record.rawMaterialId,
            finishedProductId=record.finishedProductId,
            quantityProduced=record.quantityProduced,
            createdAt=record.createdAt,
            updatedAt=record.updatedAt,
        )
        for record in records
    ]
    return GetAllProductionRecordsResponse(records=response_records)
