from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class CreateCustomerResponse(BaseModel):
    """
    Response model returning the details of the newly created customer. This aids in confirming the entry of the customer into the system.
    """

    id: str
    name: str
    email: str
    phone: str
    address: Optional[str] = None
    createdAt: datetime


async def createCustomer(
    name: str, email: str, phone: str, address: Optional[str]
) -> CreateCustomerResponse:
    """
    Creates a new customer record. This route captures essential customer details and stores them into the system. It is used every time a new customer is onboarded into the system.

    Args:
    name (str): Full name of the customer. This is a required field.
    email (str): Email address of the customer. Must be unique across all customers.
    phone (str): Phone number of the customer. Also needs to be unique.
    address (Optional[str]): Physical address of the customer. This field is optional.

    Returns:
    CreateCustomerResponse: Response model returning the details of the newly created customer. This aids in confirming the entry of the customer into the system.

    Raises:
    - ValueError: If email or phone already exists to ensure uniqueness constraint.
    """
    existing_customer_email = await prisma.models.CustomerContact.prisma().find_unique(
        where={"email": email}
    )
    if existing_customer_email:
        raise ValueError("Email already in use.")
    existing_customer_phone = await prisma.models.CustomerContact.prisma().find_unique(
        where={"phone": phone}
    )
    if existing_customer_phone:
        raise ValueError("Phone number already in use.")
    customer_contact = await prisma.models.CustomerContact.prisma().create(
        data={"name": name, "email": email, "phone": phone, "address": address}
    )
    return CreateCustomerResponse(
        id=customer_contact.id,
        name=customer_contact.name,
        email=customer_contact.email,
        phone=customer_contact.phone,
        address=customer_contact.address,
        createdAt=customer_contact.createdAt,
    )
