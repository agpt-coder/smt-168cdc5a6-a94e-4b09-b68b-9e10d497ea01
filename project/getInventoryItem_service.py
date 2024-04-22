from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class InventoryDetails(BaseModel):
    """
    A complex type to handle the specifics of both raw materials and finished products.
    """

    dimensions: Optional[str] = None
    materialType: Optional[str] = None
    quantity: float
    unit: str
    grade: Optional[str] = None


class InventoryItemResponse(BaseModel):
    """
    A response model designed to provide detailed data about a specific inventory item. It covers both raw materials and finished goods, providing flexibility in handling various types of inventory.
    """

    itemType: str
    details: InventoryDetails


async def getInventoryItem(itemId: str) -> InventoryItemResponse:
    """
    Fetches detailed information of a specific inventory item by its ID. It shows detailed information such as the dimensions, material type, and quantity available. This detailed view assists in precise operations and planning.

    Args:
        itemId (str): Unique identifier for the inventory item; can refer to either a raw material or a finished product.

    Returns:
        InventoryItemResponse: A response model designed to provide detailed data about a specific inventory item. It covers both raw materials and finished goods, providing flexibility in handling various types of inventory.

    Example:
        getInventoryItem('some-raw-material-id')
        > InventoryItemResponse(itemType='RawMaterial', details=InventoryDetails(dimensions='100x200', materialType='Wood', quantity=30, unit='Pieces', grade=None))

        getInventoryItem('some-finished-product-id')
        > InventoryItemResponse(itemType='FinishedProduct', details=InventoryDetails(dimensions='150x250', materialType=None, quantity=20, unit='Pieces', grade='A+'))

    Note: This function combines details from two models: RawMaterial and FinishedProduct. The specific model queried depends on the itemId prefix or any other distinguishing features used in your data model system.
    """
    raw_material = await prisma.models.RawMaterial.prisma().find_unique(
        where={"id": itemId}
    )
    finished_product = await prisma.models.FinishedProduct.prisma().find_unique(
        where={"id": itemId}
    )
    if raw_material:
        details = InventoryDetails(
            dimensions=None,
            materialType=raw_material.type,
            quantity=raw_material.quantity,
            unit=raw_material.unit,
            grade=None,
        )
        return InventoryItemResponse(itemType="RawMaterial", details=details)
    elif finished_product:
        details = InventoryDetails(
            dimensions=None,
            materialType=None,
            quantity=finished_product.quantity,
            unit=finished_product.unit,
            grade=finished_product.grade,
        )
        return InventoryItemResponse(itemType="FinishedProduct", details=details)
    raise ValueError("No inventory item found with the provided ID")
