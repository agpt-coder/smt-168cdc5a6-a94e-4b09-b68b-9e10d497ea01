from datetime import datetime
from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class ProductSalesData(BaseModel):
    """
    Sales information for a specific product including total revenue and dates.
    """

    product_id: str
    total_revenue: float
    sales_dates: List[datetime]


class SalesReportResponse(BaseModel):
    """
    Sales report data categorized by product and date showing total revenue.
    """

    reports: List[ProductSalesData]


async def getSalesReport(
    start_date: datetime, end_date: datetime, product_id: Optional[str] = None
) -> SalesReportResponse:
    """
    Generates a sales report based on data from the Sales and Invoicing Module. It summarizes total sales revenue, categorized by product and date. The response is typically in JSON, listing each product along with total sales and associated dates.

    Args:
        start_date (datetime): The starting date of the report period.
        end_date (datetime): The ending date of the report period.
        product_id (Optional[str]): Optional product ID to filter the sales report by a specific product.

    Returns:
        SalesReportResponse: Sales report data categorized by product and date showing total revenue.
    """
    invoices = await prisma.models.Invoice.prisma().find_many(
        where={"issueDate": {"gte": start_date, "lte": end_date}},
        include={"CustomerContact": True},
    )
    sales_data = {}
    for invoice in invoices:
        if not product_id or product_id == invoice.CustomerContact.id:
            if invoice.CustomerContact.id not in sales_data:
                sales_data[invoice.CustomerContact.id] = {
                    "total_revenue": 0,
                    "sales_dates": [],
                }
            sales_data[invoice.CustomerContact.id][
                "total_revenue"
            ] += invoice.totalAmount
            sales_data[invoice.CustomerContact.id]["sales_dates"].append(
                invoice.issueDate
            )
    report_response = SalesReportResponse(
        reports=[
            ProductSalesData(
                product_id=product_id,
                total_revenue=data["total_revenue"],
                sales_dates=data["sales_dates"],
            )
            for product_id, data in sales_data.items()
        ]
    )
    return report_response
