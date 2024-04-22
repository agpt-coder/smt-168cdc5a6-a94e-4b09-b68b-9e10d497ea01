from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class MaintenanceLogDetailsResponse(BaseModel):
    """
    This model represents the detailed response containing data about a specific maintenance log. It wraps the MaintenanceLog data returned from the database with additional information if necessary.
    """

    logId: str
    userId: str
    description: str
    date: datetime
    nextDueDate: datetime
    createdAt: datetime
    updatedAt: datetime


async def getMaintenanceLog(logId: str) -> MaintenanceLogDetailsResponse:
    """
    Fetches detailed information about a specific maintenance log identified by the logId. Useful for drilling down into individual maintenance records for debug or audit purposes. Ensures data is up-to-date before presentation.

    Args:
        logId (str): The unique identifier for the maintenance log to be retrieved. This ID is used to look up the specific log in the database.

    Returns:
        MaintenanceLogDetailsResponse: This model represents the detailed response containing data about a specific maintenance log. It wraps the MaintenanceLog data returned from the database with additional information if necessary.
    """
    log = await prisma.models.MaintenanceLog.prisma().find_unique(
        where={"id": logId}, include={"User": True}
    )
    if log is None:
        raise ValueError("Maintenance log not found with the given log ID.")
    response = MaintenanceLogDetailsResponse(
        logId=log.id,
        userId=log.userId,
        description=log.description,
        date=log.date,
        nextDueDate=log.nextDueDate,
        createdAt=log.createdAt,
        updatedAt=log.updatedAt,
    )
    return response
