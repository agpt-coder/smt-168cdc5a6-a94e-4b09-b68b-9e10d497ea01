from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class RawMaterialData(BaseModel):
    """
    Detailed information about each type of raw material in stock.
    """

    type: str
    quantity: int
    unit: str


class FinishedProductData(BaseModel):
    """
    Detailed information on each type of finished product in stock.
    """

    type: str
    quantity: int
    unit: str
    grade: str


class InventoryLevels(BaseModel):
    """
    Provides a comprehensive list of both raw materials and finished products currently in stock.
    """

    raw_materials: List[RawMaterialData]
    finished_products: List[FinishedProductData]


async def listInventory(
    material_type: Optional[str], product_type: Optional[str]
) -> InventoryLevels:
    """
    Displays current stock levels of raw materials and finished products. This endpoint is crucial for inventory tracking in real-time.

    Args:
        material_type (Optional[str]): Optional filter for the type of raw materials.
        product_type (Optional[str]): Optional filter for the type of finished products.

    Returns:
        InventoryLevels: Provides a comprehensive list of both raw materials and finished products currently in stock.
    """
    query_materials = prisma.models.RawMaterial.prisma()
    query_products = prisma.models.FinishedProduct.prisma()
    if material_type:
        raw_materials = await query_materials.find_many(where={"type": material_type})
    else:
        raw_materials = await query_materials.find_many()
    if product_type:
        finished_products = await query_products.find_many(where={"type": product_type})
    else:
        finished_products = await query_products.find_many()
    raw_material_data = [
        RawMaterialData(type=rm.type, quantity=rm.quantity, unit=rm.unit)
        for rm in raw_materials
    ]
    finished_product_data = [
        FinishedProductData(
            type=fp.type, quantity=fp.quantity, unit=fp.unit, grade=fp.grade
        )
        for fp in finished_products
    ]
    return InventoryLevels(
        raw_materials=raw_material_data, finished_products=finished_product_data
    )
