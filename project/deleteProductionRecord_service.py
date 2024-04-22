from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class DeleteProductionRecordResponse(BaseModel):
    """
    This model will confirm the deletion of the production record or relay error information.
    """

    success: bool
    message: Optional[str] = None


async def deleteProductionRecord(recordId: str) -> DeleteProductionRecordResponse:
    """
    Removes a specific production record from the database. This might be necessary in cases of errors or duplication.

    Args:
    recordId (str): The unique identifier of the production record intended for deletion.

    Returns:
    DeleteProductionRecordResponse: This model will confirm the deletion of the production record or relay error information.
    """
    try:
        record = await prisma.models.ProductionRecord.prisma().delete(
            where={"id": recordId}
        )
        return DeleteProductionRecordResponse(
            success=True,
            message=f"Production record with ID {recordId} was successfully deleted.",
        )
    except Exception as e:
        return DeleteProductionRecordResponse(success=False, message=str(e))
