from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class InventoryItem(BaseModel):
    """
    Detailed model for an individual inventory item, which may be a raw material or finished product.
    """

    id: str
    type: str
    quantity: int
    unit: str
    status: str


class InventoryResponse(BaseModel):
    """
    Response model for the inventory tracking endpoint. It provides a list of both raw materials and finished products, detailing their type, quantity, and status.
    """

    inventory_items: List[InventoryItem]


async def getInventoryList(
    item_type: Optional[str], status: Optional[str]
) -> InventoryResponse:
    """
    Retrieves a list of all inventory items including both raw materials and finished products. The data provided will include item types, quantities, and status. This route is crucial for providing constant inventory updates to the Production Recording and Price Estimation Modules.

    Args:
        item_type (Optional[str]): Filter by type of item, either 'RawMaterial' or 'FinishedProduct'. This parameter is optional.
        status (Optional[str]): Filter the inventory items based on their status. Possible status values might include 'in-stock', 'low-stock', 'out-of-stock'. This parameter is optional.

    Returns:
        InventoryResponse: Response model for the inventory tracking endpoint. It provides a list of both raw materials and finished products, detailing their type, quantity, and status.
    """
    query_criteria_raw = {}
    query_criteria_finished = {}
    if item_type:
        if item_type == "RawMaterial":
            query_criteria_raw["type"] = item_type
        elif item_type == "FinishedProduct":
            query_criteria_finished["type"] = item_type
    if status and status == "in-stock":
        query_criteria_raw["quantity"] = {"gt": 0}
        query_criteria_finished["quantity"] = {"gt": 0}
    elif status and status == "low-stock":
        query_criteria_raw["quantity"] = {"lte": 10}
        query_criteria_finished["quantity"] = {"lte": 5}
    elif status and status == "out-of-stock":
        query_criteria_raw["quantity"] = 0
        query_criteria_finished["quantity"] = 0
    raw_materials = await prisma.models.RawMaterial.prisma().find_many(
        where=query_criteria_raw
    )
    finished_products = await prisma.models.FinishedProduct.prisma().find_many(
        where=query_criteria_finished
    )
    inventory_items = []
    for raw_material in raw_materials:
        inventory_items.append(
            InventoryItem(
                id=raw_material.id,
                type="RawMaterial",
                quantity=raw_material.quantity,
                unit=raw_material.unit,
                status="in-stock" if raw_material.quantity > 0 else "out-of-stock",
            )
        )
    for finished_product in finished_products:
        inventory_items.append(
            InventoryItem(
                id=finished_product.id,
                type="FinishedProduct",
                quantity=finished_product.quantity,
                unit=finished_product.unit,
                status="in-stock" if finished_product.quantity > 0 else "out-of-stock",
            )
        )
    return InventoryResponse(inventory_items=inventory_items)
