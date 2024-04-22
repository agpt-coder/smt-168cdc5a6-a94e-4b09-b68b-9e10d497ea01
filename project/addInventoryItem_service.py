from typing import Dict

import prisma
import prisma.models
from pydantic import BaseModel


class AddInventoryResponse(BaseModel):
    """
    Response model indicating successful addition of an inventory item.
    """

    message: str


async def addInventoryItem(
    type: str, quantity: int, dimensions: Dict[str, float], unit: str
) -> AddInventoryResponse:
    """
    Allows the addition of a new inventory item. This is utilized when new stock comes in or when a new type of material or product is introduced into the inventory. It inputs data like type, quantity, and dimensions.

    Args:
        type (str): The type of item being added to the inventory, e.g., 'prisma.models.RawMaterial' or 'prisma.models.FinishedProduct'.
        quantity (int): The quantity of the item being added to the stock.
        dimensions (Dict[str, float]): Dimensions of the item if applicable. Should be in dictionary format including height, width, and depth where applicable.
        unit (str): Unit of measure for the quantity, e.g., 'cubic meters', 'kilograms', etc.

    Returns:
        AddInventoryResponse: Response model indicating successful addition of an inventory item.

    Example:
        addInventoryItem('prisma.models.RawMaterial', 100, {'height': 2.0, 'width': 1.0, 'depth': 0.5}, 'cubic meters')
        > {'message': 'prisma.models.RawMaterial successfully added to inventory.'}
    """
    if type.lower() == "rawmaterial":
        model = prisma.models.RawMaterial
    elif type.lower() == "finishedproduct":
        model = prisma.models.FinishedProduct
    else:
        raise ValueError(
            "Unsupported inventory type. Valid types are 'prisma.models.RawMaterial' and 'prisma.models.FinishedProduct'."
        )
    await model.prisma().create({"type": type, "quantity": quantity, "unit": unit})
    return AddInventoryResponse(message=f"{type} successfully added to inventory.")
