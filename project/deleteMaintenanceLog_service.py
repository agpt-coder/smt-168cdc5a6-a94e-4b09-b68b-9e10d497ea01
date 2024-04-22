import prisma
import prisma.models
from pydantic import BaseModel


class DeleteMaintenanceLogResponse(BaseModel):
    """
    Response model indicating successful deletion of a maintenance log entry.
    """

    success: bool
    message: str


async def deleteMaintenanceLog(logId: str) -> DeleteMaintenanceLogResponse:
    """
    Deletes a maintenance log, used typically when a log entry has been erroneously created or if maintenance cancellation is confirmed. Removes the record permanently ensuring data integrity and database cleanliness.

    Args:
        logId (str): The unique identifier for the maintenance log entry that is to be deleted.

    Returns:
        DeleteMaintenanceLogResponse: Response model indicating successful deletion of a maintenance log entry.

    Example:
        response = deleteMaintenanceLog('abc123-log-id')
        > {'success': True, 'message': 'Maintenance log deleted successfully'}
    """
    try:
        log = await prisma.models.MaintenanceLog.prisma().find_unique(
            where={"id": logId}
        )
        if log is None:
            return DeleteMaintenanceLogResponse(
                success=False, message="No maintenance log found with the given ID."
            )
        await prisma.models.MaintenanceLog.prisma().delete(where={"id": logId})
        return DeleteMaintenanceLogResponse(
            success=True, message="Maintenance log deleted successfully."
        )
    except Exception as e:
        return DeleteMaintenanceLogResponse(
            success=False, message=f"Failed to delete maintenance log: {str(e)}"
        )
