from datetime import date
from typing import Any, Dict, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class ProductionReportResponse(BaseModel):
    """
    Structured response containing production data grouped by date and shift.
    """

    date: date
    shift: str
    total_volume: float
    yield_percentage: float
    additional_details: Optional[Dict[str, Any]] = None


async def filter_records(
    start_date: date, end_date: date, shift: Optional[str], product_type: Optional[str]
):
    """
    Filter production records within the given time range, shift, and product type.

    Args:
        start_date (date): The starting date for the report range.
        end_date (date): The ending date for the report range.
        shift (Optional[str]): Optional shift identifier.
        product_type (Optional[str]): Optional product type.

    Returns:
        List of records that match the criteria.
    """
    query_parameters = {
        "createdAt": {"gte": start_date, "lte": end_date},
        **({"shift": shift} if shift else {}),
        **({"type": product_type} if product_type else {}),
    }
    return await prisma.models.ProductionRecord.prisma().find_many(
        where=query_parameters
    )


async def getProductionReport(
    start_date: date, end_date: date, shift: Optional[str], product_type: Optional[str]
) -> ProductionReportResponse:
    """
    Retrieves production reports showing daily volumes and yields. This route gathers data from the Production Recording Module, processes it, and presents a structured report. Expected responses include data groupings by date and shift, possibly in JSON format containing fields like date, total volume, and yield percentage.

    Args:
        start_date (date): The starting date for the report range.
        end_date (date): The ending date for the report range.
        shift (Optional[str]): Optional shift identifier to filter the report by specific work shifts.
        product_type (Optional[str]): Optional product type to filter the report for specific products.

    Returns:
        ProductionReportResponse: Structured response containing production data grouped by date and shift.
    """
    records = await filter_records(start_date, end_date, shift, product_type)
    total_volume = sum((record.quantityProduced for record in records))
    average_yield = sum(
        (
            record.quantityProduced / record.FinishedProduct.quantity * 100
            for record in records
        )
    ) / len(records)
    return ProductionReportResponse(
        date=start_date,
        shift=shift if shift else "All Shifts",
        total_volume=total_volume,
        yield_percentage=average_yield,
        additional_details={
            "product_type": product_type if product_type else "All Types",
            "number_of_days": (end_date - start_date).days + 1,
        },
    )
