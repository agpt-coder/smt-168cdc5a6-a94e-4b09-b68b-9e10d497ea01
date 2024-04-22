from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class CustomerContact(BaseModel):
    """
    This is a model representing a customer contact stored in the system.
    """

    id: str
    userId: str
    name: str
    address: Optional[str] = None
    phone: str
    email: str
    createdAt: datetime
    updatedAt: datetime


class GetInvoiceResponse(BaseModel):
    """
    This model structures the detailed information of an invoice, retrieved based on the provided invoice ID, for clear and organized financial tracking and management.
    """

    id: str
    customerContactId: str
    createdAt: datetime
    updatedAt: datetime
    issueDate: datetime
    dueDate: datetime
    totalAmount: float
    customerContact: CustomerContact


async def getInvoice(invoiceId: str) -> GetInvoiceResponse:
    """
    Accesses detailed information on a specific invoice, enabling financial tracking and management for sales transactions.

    Args:
        invoiceId (str): The unique identifier of the invoice to retrieve details for.

    Returns:
        GetInvoiceResponse: This model structures the detailed information of an invoice,
        retrieved based on the provided invoice ID, for clear and organized financial tracking and management.
    """
    invoice = await prisma.models.Invoice.prisma().find_unique(
        where={"id": invoiceId}, include={"CustomerContact": True}
    )
    if not invoice:
        raise ValueError(f"No invoice found with ID: {invoiceId}")
    response = GetInvoiceResponse(
        id=invoice.id,
        customerContactId=invoice.customerContactId,
        createdAt=invoice.createdAt,
        updatedAt=invoice.updatedAt,
        issueDate=invoice.issueDate,
        dueDate=invoice.dueDate,
        totalAmount=invoice.totalAmount,
        customerContact=CustomerContact(
            id=invoice.CustomerContact.id,
            userId=invoice.CustomerContact.userId,
            name=invoice.CustomerContact.name,
            address=invoice.CustomerContact.address,
            phone=invoice.CustomerContact.phone,
            email=invoice.CustomerContact.email,
            createdAt=invoice.CustomerContact.createdAt,
            updatedAt=invoice.CustomerContact.updatedAt,
        ),
    )
    return response
