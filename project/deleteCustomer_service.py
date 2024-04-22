import prisma
import prisma.models
from pydantic import BaseModel


class DeleteCustomerResponse(BaseModel):
    """
    Confirmation of the successful deletion of a customer record or providing error context if the operation fails.
    """

    success: bool
    message: str


async def deleteCustomer(customerId: str) -> DeleteCustomerResponse:
    """
    Removes a customer's record from the system. This is a critical function restricted to users who manage data accuracy and relevancy in customer relationships.

    Args:
        customerId (str): The unique identifier of the customer to be deleted from the system.

    Returns:
        DeleteCustomerResponse: Confirmation of the successful deletion of a customer record or providing error context if the operation fails.
    """
    try:
        customer = await prisma.models.CustomerContact.prisma().find_unique(
            where={"id": customerId}
        )
        if customer is None:
            return DeleteCustomerResponse(success=False, message="Customer not found.")
        await prisma.models.CustomerContact.prisma().delete(where={"id": customerId})
        return DeleteCustomerResponse(
            success=True, message="Customer successfully deleted."
        )
    except Exception as e:
        return DeleteCustomerResponse(
            success=False, message=f"Error while deleting the customer: {str(e)}"
        )
