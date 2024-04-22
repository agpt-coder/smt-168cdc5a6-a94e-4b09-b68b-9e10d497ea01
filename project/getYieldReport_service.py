from datetime import datetime
from typing import Dict, List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class ProductionRecord(BaseModel):
    """
    Individual records for each production log entry, detailing outputs and resource utilization.
    """

    id: str
    quantityProduced: int
    rawMaterialUsage: Dict[str, int]


class YieldDataResponse(BaseModel):
    """
    This response model packages the yield data retrieved from the ProductionRecord modules into a clear and concise format. It includes computation for the yield percentage.
    """

    batch_id: str
    yield_percentage: float
    start_date: datetime
    end_date: datetime
    records: List[ProductionRecord]


async def getYieldReport(
    batch_id: Optional[str],
    start_date: Optional[datetime],
    end_date: Optional[datetime],
) -> YieldDataResponse:
    """
    Fetches yield data, crucial for evaluating operational efficiency, particularly by processing information from the Production Recording Module.

    Args:
        batch_id (Optional[str]): The batch ID to filter the yield reports by. If None, fetches all records.
        start_date (Optional[datetime]): The start date for the period over which yield data is filtered. If None, no start date filter applied.
        end_date (Optional[datetime]): The end date for the period over which yield data is filtered. If None, no end date filter applied.

    Returns:
        YieldDataResponse: This encapsulates the yield data retrieved. It summarizes the information along with a computed yield percentage.
    """
    where_clauses = {}
    if batch_id:
        where_clauses["batch_id"] = batch_id
    if start_date:
        where_clauses["createdAt"] = {"gte": start_date}
    if end_date:
        where_clauses["updatedAt"] = {"lte": end_date}
    records = await prisma.models.ProductionRecord.prisma().find_many(
        where=where_clauses
    )
    total_quantity_produced = sum((record.quantityProduced for record in records))
    total_raw_material_used = sum((record.quantityProduced for record in records))
    yield_percentage = (
        total_quantity_produced / total_raw_material_used * 100
        if total_raw_material_used
        else 0
    )
    response_data = YieldDataResponse(
        batch_id=batch_id or "All",
        yield_percentage=yield_percentage,
        start_date=start_date,
        end_date=end_date,
        records=[ProductionRecord(**record.__dict__) for record in records],
    )
    return response_data
