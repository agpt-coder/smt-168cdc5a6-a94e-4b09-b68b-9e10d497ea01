from datetime import datetime
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class InvoiceResponse(BaseModel):
    """
    This model defines the structure for the response after creating an invoice, containing detailed invoice data.
    """

    invoiceId: str
    customerContactId: str
    totalAmount: float
    issueDate: datetime
    dueDate: datetime


async def createInvoice(
    customerContactId: str, quoteIds: List[str], issueDate: datetime, dueDate: datetime
) -> InvoiceResponse:
    """
    Issues an invoice based on the final agreement and quotes approved by the customer. This is crucial for official documentation and billing purposes.

    Args:
        customerContactId (str): Unique identifier for the customer contact to relate this invoice.
        quoteIds (List[str]): List of quote identifiers which are approved by customer and used for this invoice.
        issueDate (datetime): Date when the invoice is officially issued.
        dueDate (datetime): Date by which the payment for this invoice should be completed.

    Returns:
        InvoiceResponse: This model defines the structure for the response after creating an invoice, containing detailed invoice data.
    """
    total_amount = 0.0
    for quote_id in quoteIds:
        quote = await prisma.models.Quote.prisma().find_unique(where={"id": quote_id})
        for price_estimate in quote.priceEstimate:
            total_amount += price_estimate.priceRate * price_estimate.quantity
    new_invoice = await prisma.models.Invoice.prisma().create(
        data={
            "customerContactId": customerContactId,
            "issueDate": issueDate,
            "dueDate": dueDate,
            "totalAmount": total_amount,
        }
    )
    return InvoiceResponse(
        invoiceId=new_invoice.id,
        customerContactId=customerContactId,
        totalAmount=total_amount,
        issueDate=issueDate,
        dueDate=dueDate,
    )
