from typing import Type

import prisma
import prisma.models
from pydantic import BaseModel


class DeleteInventoryItemResponse(BaseModel):
    """
    Response model for confirming deletion of an inventory item. Provides feedback on the success of the operation and connects to the security if deletion was not permitted.
    """

    message: str
    deletedItemId: str
    status: str


async def deleteInventoryItem(
    itemId: str, itemType: Type[str]
) -> DeleteInventoryItemResponse:
    """
    Deletes a specific item from the inventory when it is no longer needed or errorneously entered. This keeps the inventory data clean and accurate, helping avoid any operational discrepancies.

    Args:
        itemId (str): The unique identifier for the inventory item to be deleted. Can refer to either a RawMaterial or a FinishedProduct.
        itemType (Type[str]): The type of the item to be deleted, distinguishing between 'RawMaterial' and 'FinishedProduct'.

    Returns:
        DeleteInventoryItemResponse: Response model for confirming deletion of an inventory item. Provides feedback on the success of the operation and connects to the security if deletion was not permitted.

    Example:
        deleteInventoryItem("some_id", 'RawMaterial')
        > DeleteInventoryItemResponse(message="Item deleted successfully", deletedItemId="some_id", status="200 OK")
    """
    if itemType not in ["RawMaterial", "FinishedProduct"]:
        return DeleteInventoryItemResponse(
            message="Invalid item type specified.",
            deletedItemId="",
            status="400 Bad Request",
        )
    model = (
        prisma.models.RawMaterial
        if itemType == "RawMaterial"
        else prisma.models.FinishedProduct
    )
    try:
        item = await model.prisma().delete(where={"id": itemId})
        return DeleteInventoryItemResponse(
            message="Item deleted successfully", deletedItemId=itemId, status="200 OK"
        )
    except prisma.exceptions.NotFoundError:
        return DeleteInventoryItemResponse(
            message="No item found with provided ID, or deletion not allowed.",
            deletedItemId="",
            status="404 Not Found",
        )
    except prisma.exceptions.PrismaError:
        return DeleteInventoryItemResponse(
            message="Error during deletion process.",
            deletedItemId="",
            status="500 Internal Server Error",
        )
