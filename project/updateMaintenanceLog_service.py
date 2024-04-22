from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class MaintenanceLog(BaseModel):
    """
    A model representing a log entry for equipment maintenance.
    """

    id: str
    userId: str
    description: str
    date: datetime
    nextDueDate: datetime


class UpdateMaintenanceLogResponse(BaseModel):
    """
    Response model that confirms the maintenance log has been updated. Contains the updated maintenance log details.
    """

    success: bool
    updatedLog: MaintenanceLog
    message: str


async def updateMaintenanceLog(
    logId: str,
    maintenanceStatus: str,
    actualCompletionDate: datetime,
    additionalNotes: Optional[str],
) -> UpdateMaintenanceLogResponse:
    """
    Updates an existing maintenance log entry, with input fields such as maintenance status, actual completion date, and additional notes. Validates changes against business rules and updates the database record.

    Args:
        logId (str): The unique identifier of the maintenance log to be updated.
        maintenanceStatus (str): The updated status of the maintenance task, e.g., 'Completed', 'Pending', 'In Progress'.
        actualCompletionDate (datetime): The actual date when the maintenance was completed. Should be validated to ensure it's not in the future.
        additionalNotes (Optional[str]): Any additional notes that may provide context or details about the maintenance performed.

    Returns:
        UpdateMaintenanceLogResponse: Response model that confirms the maintenance log has been updated. Contains the updated maintenance log details.
    """
    maintenance_log = await prisma.models.MaintenanceLog.prisma().find_unique(
        where={"id": logId}
    )
    if maintenance_log and actualCompletionDate <= datetime.now():
        update_data = {
            "description": maintenanceStatus,
            "date": maintenance_log.date,
            "nextDueDate": actualCompletionDate,
        }
        if additionalNotes is not None:
            update_data["description"] += "\nNotes: " + additionalNotes
        updated_log = await prisma.models.MaintenanceLog.prisma().update(
            where={"id": logId}, data=update_data
        )
        return UpdateMaintenanceLogResponse(
            success=True,
            updatedLog=MaintenanceLog.parse_obj(updated_log),
            message="Maintenance log updated successfully.",
        )
    else:
        message = "Invalid log ID or future completion date provided."
        if not maintenance_log:
            message = "Maintenance log not found."
        return UpdateMaintenanceLogResponse(
            success=False,
            updatedLog=MaintenanceLog.parse_obj(maintenance_log)
            if maintenance_log
            else None,
            message=message,
        )
