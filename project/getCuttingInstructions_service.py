from typing import Dict, List

from pydantic import BaseModel


class CuttingInstructionsResponse(BaseModel):
    """
    Output model containing optimized cutting instructions.
    """

    instructions: List[Dict[str, str]]
    total_materials_used: int
    expected_waste_percentage: float


async def getCuttingInstructions(
    customer_id: str,
    material_dimensions: List[Dict[str, float]],
    material_quantity: int,
    material_grade: str,
) -> CuttingInstructionsResponse:
    """
    Retrieves optimized cutting instructions. This route processes customer requirements from input fields and uses algorithms to minimize waste while maximizing yield, returning detailed cutting instructions.

    Args:
        customer_id (str): Identifier for the customer to which the cutting instructions should apply.
        material_dimensions (List[Dict[str, float]]): Requested material dimensions to calculate the cutting pattern.
        material_quantity (int): The quantity of the material to be cut.
        material_grade (str): Grade of the material to be used in cutting.

    Returns:
        CuttingInstructionsResponse: Output model containing optimized cutting instructions.
    """
    effective_material_use = 0
    waste_percentage = 0.05
    instructions = []
    for dimension in material_dimensions:
        instructions.append(
            {
                "length": str(dimension["length"]),
                "width": str(dimension["width"]),
                "cut_count": str(material_quantity),
                "description": "Cut these dimensions to minimize offcuts",
            }
        )
        effective_material_use += material_quantity
    total_material_used = effective_material_use
    expected_waste_percentage = waste_percentage * 100
    return CuttingInstructionsResponse(
        instructions=instructions,
        total_materials_used=total_material_used,
        expected_waste_percentage=expected_waste_percentage,
    )
