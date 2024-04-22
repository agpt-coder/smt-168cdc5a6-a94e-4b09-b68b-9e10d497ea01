from typing import List, Tuple

import prisma
import prisma.models
from pydantic import BaseModel


class ProductionDataResponse(BaseModel):
    """
    Response after logging a production entry. Confirms the creation of the production log.
    """

    success: bool
    productionRecordId: str
    message: str


async def recordProduction(
    userId: str,
    rawMaterialId: str,
    finishedProductId: str,
    quantityProduced: int,
    lumberDimensions: List[Tuple[int, int, int]],
    lumberGrade: str,
) -> ProductionDataResponse:
    """
    Stores daily production data including quantities, dimensions, and grades of lumber produced. Essential for production tracking and reporting.

    Args:
        userId (str): Identifier for the user logging the production. Should correspond to an existing user in the 'User' DB model.
        rawMaterialId (str): Identifier for the raw material used in the production. Must match an existing raw material entry in the database.
        finishedProductId (str): Identifier for the finished lumber product produced. Should link to the 'FinishedProduct' model for specifics like grade and dimensions.
        quantityProduced (int): The total quantity of finished products produced in this record.
        lumberDimensions (List[Tuple[int, int, int]]): List of dimensions of lumber produced. This field allows recording different sizes made during a production cycle.
        lumberGrade (str): Grade of the lumber produced, categorized by quality e.g., A, B, C.

    Returns:
        ProductionDataResponse: Response after logging a production entry. Confirms the creation of the production log.
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": userId})
    if not user:
        return ProductionDataResponse(
            success=False,
            productionRecordId="",
            message="No user found with provided UserId.",
        )
    raw_material = await prisma.models.RawMaterial.prisma().find_unique(
        where={"id": rawMaterialId}
    )
    if not raw_material:
        return ProductionDataResponse(
            success=False,
            productionRecordId="",
            message="No raw material found with provided RawMaterialId.",
        )
    finished_product = await prisma.models.FinishedProduct.prisma().find_unique(
        where={"id": finishedProductId}
    )
    if not finished_product:
        return ProductionDataResponse(
            success=False,
            productionRecordId="",
            message="No finished product found with provided FinishedProductId.",
        )
    lumber_dimension_str = str(lumberDimensions)
    new_production_record = await prisma.models.ProductionRecord.prisma().create(
        data={
            "userId": userId,
            "rawMaterialId": rawMaterialId,
            "finishedProductId": finishedProductId,
            "quantityProduced": quantityProduced,
            "lumberGrade": lumberGrade,
            "lumberDimensions": lumber_dimension_str,
        }
    )
    if new_production_record:
        return ProductionDataResponse(
            success=True,
            productionRecordId=new_production_record.id,
            message="Production data successfully recorded.",
        )
    else:
        return ProductionDataResponse(
            success=False,
            productionRecordId="",
            message="Failed to record production data.",
        )
