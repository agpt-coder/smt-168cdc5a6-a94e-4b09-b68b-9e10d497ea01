from datetime import datetime

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class MaintenanceLogCreateResponse(BaseModel):
    """
    Response model representing a newly created maintenance log entry.
    """

    log_id: str
    equipment_id: str
    details: str
    scheduled_date: datetime
    status: str


async def createMaintenanceLog(
    equipment_id: str,
    details: str,
    scheduled_date: datetime,
    maintenance_manager_id: str,
) -> MaintenanceLogCreateResponse:
    """
    Creates a new log entry for equipment maintenance. Data inputs include equipment ID, maintenance details, and scheduled dates. Validates input data for consistency and stores the entry in the database. Ensures only maintenance personnel can update logs.

    Args:
        equipment_id (str): Unique identifier for the equipment.
        details (str): Detailed description of the maintenance tasks to be performed.
        scheduled_date (datetime): The date when the maintenance is scheduled to occur.
        maintenance_manager_id (str): The ID of the maintenance manager who is logging this maintenance entry.

    Returns:
        MaintenanceLogCreateResponse: Response model representing a newly created maintenance log entry.
    """
    manager = await prisma.models.User.prisma().find_unique(
        where={"id": maintenance_manager_id}
    )
    if not manager or manager.role != prisma.enums.Role.MAINTENANCE_MANAGER:
        return MaintenanceLogCreateResponse(
            log_id="",
            equipment_id="",
            details="",
            scheduled_date=scheduled_date,
            status="Failed: Unauthorized action or manager not found",
        )
    created_log = await prisma.models.MaintenanceLog.prisma().create(
        data={
            "userId": maintenance_manager_id,
            "description": details,
            "date": scheduled_date,
            "nextDueDate": scheduled_date,
        }
    )
    return MaintenanceLogCreateResponse(
        log_id=created_log.id,
        equipment_id=equipment_id,
        details=details,
        scheduled_date=scheduled_date,
        status="Success",
    )
