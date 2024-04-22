from datetime import datetime
from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class GetCustomersInput(BaseModel):
    """
    Input for retrieving all customer contacts involves no parameters as we are simply performing a list operation over the resource.
    """

    pass


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


class GetCustomersOutput(BaseModel):
    """
    Outputs the collection of all customer contacts.
    """

    customers: List[CustomerContact]


async def listCustomers(request: GetCustomersInput) -> GetCustomersOutput:
    """
    Retrieves a list of all customers stored in the system. This is used by sales personnel to access customer contacts and manage relationships.

    Args:
        request (GetCustomersInput): Input for retrieving all customer contacts involves no parameters as we are simply performing a list operation over the resource.

    Returns:
        GetCustomersOutput: Outputs the collection of all customer contacts.
    """
    customer_contacts = await prisma.models.CustomerContact.prisma().find_many()
    customers_list = [
        prisma.models.CustomerContact(
            id=contact.id,
            userId=contact.userId,
            name=contact.name,
            address=contact.address,
            phone=contact.phone,
            email=contact.email,
            createdAt=contact.createdAt,
            updatedAt=contact.updatedAt,
        )
        for contact in customer_contacts
    ]
    output = GetCustomersOutput(customers=customers_list)
    return output
