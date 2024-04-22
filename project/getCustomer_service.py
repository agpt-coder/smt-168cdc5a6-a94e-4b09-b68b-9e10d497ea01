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


class CustomerDetailsResponse(BaseModel):
    """
    This model provides a comprehensive dataset concerning the customer, including contact details, quotes, and invoices. It is designed to give a complete view of the customer's engagements and transactions for sales and administrative processes.
    """

    customer: CustomerContact


async def getCustomer(customerId: str) -> CustomerDetailsResponse:
    """
    Fetches detailed information for a particular customer using their unique identifier. This is essential for editing customer details and understanding customer engagement history.

    Args:
    customerId (str): The unique identifier of the customer whose details are being requested.

    Returns:
    CustomerDetailsResponse: This model provides a comprehensive dataset concerning the customer, including contact details, quotes, and invoices. It is designed to give a complete view of the customer's engagements and transactions for sales and administrative processes.
    """
    customer = await prisma.models.CustomerContact.prisma().find_unique(
        where={"id": customerId}, include={"Quotes": True, "Invoices": True}
    )
    if not customer:
        raise ValueError(f"No customer found with ID: {customerId}")
    return CustomerDetailsResponse(customer=customer)
