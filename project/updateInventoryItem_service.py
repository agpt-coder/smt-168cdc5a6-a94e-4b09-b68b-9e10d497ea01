from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdatedInventoryItem(BaseModel):
    """
    Model representing the new state of either a RawMaterial or FinishedProduct after an update.
    """

    itemId: str
    quantity: int
    dimensions: Optional[str] = None
    type: str


class UpdateInventoryItemResponse(BaseModel):
    """
    Response after updating the inventory item. Provides confirmation and details of the updated item.
    """

    success: bool
    updatedItem: UpdatedInventoryItem


async def updateInventoryItem(
    itemId: str, quantity: int, dimensions: Optional[str], type: str
) -> UpdateInventoryItemResponse:
    """
    Updates existing inventory item information such as quantity, dimensions, or type. This endpoint is fundamental after any stock adjustment or post-production update, ensuring the data remains consistent across modules.

    Args:
        itemId (str): The unique identifier for the inventory item to update. This ID should correspond either to a prisma.models.RawMaterial or prisma.models.FinishedProduct.
        quantity (int): The new quantity for the inventory item. This value is expected to be updated based on production operations or inventory auditing.
        dimensions (Optional[str]): Updated dimensions of the inventory item. This is more relevant for finished products.
        type (str): The type of material or product, which might be updated if categorization standards change.

    Returns:
        UpdateInventoryItemResponse: Response after updating the inventory item. Provides confirmation and details of the updated item.
    """
    if type.lower().startswith("raw"):
        model = prisma.models.RawMaterial
    else:
        model = prisma.models.FinishedProduct
    item = await model.prisma().find_unique(where={"id": itemId})
    if not item:
        return UpdateInventoryItemResponse(success=False, updatedItem=None)
    updated_item = await model.prisma().update(
        where={"id": itemId},
        data={
            "quantity": quantity,
            "type": type,
            **(
                {"dimensions": dimensions}
                if dimensions and model is prisma.models.FinishedProduct
                else {}
            ),
        },
    )
    updated_inventory_item = UpdatedInventoryItem(
        itemId=updated_item.id,
        quantity=updated_item.quantity,
        dimensions=getattr(updated_item, "dimensions", None),
        type=updated_item.type,
    )
    return UpdateInventoryItemResponse(success=True, updatedItem=updated_inventory_item)
