from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateCustomerResponse(BaseModel):
    """
    Confirmation response after updating a customer record.
    """

    success: bool
    customerId: str
    updatedFields: List[str]


async def updateCustomer(
    customerId: str, name: str, email: str, phone: str, address: Optional[str]
) -> UpdateCustomerResponse:
    """
    Updates specific details of an existing customer's record. This endpoint is typically used for maintaining accurate and up-to-date customer information.

    Args:
        customerId (str): The unique identifier for the customer.
        name (str): The updated name of the customer.
        email (str): The updated email address of the customer.
        phone (str): The updated telephone number of the customer.
        address (Optional[str]): The updated address of the customer, which is optional.

    Returns:
        UpdateCustomerResponse: Confirmation response after updating a customer record.
    """
    customer = await prisma.models.CustomerContact.prisma().find_unique(
        where={"id": customerId}, include={"User": True}
    )
    if customer is None:
        return UpdateCustomerResponse(
            success=False, customerId=customerId, updatedFields=[]
        )
    update_data = {}
    updated_fields = []
    if customer.name != name:
        update_data["name"] = name
        updated_fields.append("name")
    if customer.email != email:
        update_data["email"] = email
        updated_fields.append("email")
    if customer.phone != phone:
        update_data["phone"] = phone
        updated_fields.append("phone")
    if address and customer.address != address:
        update_data["address"] = address
        updated_fields.append("address")
    if update_data:
        await prisma.models.CustomerContact.prisma().update(
            where={"id": customerId}, data=update_data
        )
    return UpdateCustomerResponse(
        success=True, customerId=customerId, updatedFields=updated_fields
    )
