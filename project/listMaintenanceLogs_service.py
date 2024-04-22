from datetime import datetime
from typing import List, Optional

import prisma
import prisma.enums
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


class MaintenanceLogsResponse(BaseModel):
    """
    Provides a list of maintenance logs fetched from the database, optionally sorted. Only visible to authorized roles.
    """

    maintenance_logs: List[MaintenanceLog]


async def listMaintenanceLogs(
    sort_by: Optional[str], role: prisma.enums.Role
) -> MaintenanceLogsResponse:
    """
    Retrieves a list of all maintenance logs, allowing the Maintenance Manager to monitor scheduled and completed maintenance tasks. Uses internal queries to fetch data sorted by date, equipment, or urgency. Protection ensures only authorized personnel can view logs.

    Args:
        sort_by (Optional[str]): Determines the order of maintenance logs fetched. Accepted values can be 'date', 'equipment', and 'urgency'.
        role (Role): Role of the requesting user to verify permissions. Only 'SYSTEM_ADMINISTRATOR' and 'MAINTENANCE_MANAGER' are allowed.

    Returns:
        MaintenanceLogsResponse: Provides a list of maintenance logs fetched from the database, optionally sorted. Only visible to authorized roles.

    Raises:
        PermissionError: If the role is not authorized to view the logs.
    """
    if role not in [
        prisma.enums.Role.SYSTEM_ADMINISTRATOR,
        prisma.enums.Role.MAINTENANCE_MANAGER,
    ]:
        raise PermissionError("Not authorized to access maintenance logs.")
    query_parameters = {}
    if sort_by in ["date", "equipment", "urgency"]:
        if sort_by == "equipment":
            sort_by = "description"
        query_parameters["order"] = {sort_by: "asc"}
    maintenance_logs = await prisma.models.MaintenanceLog.prisma().find_many(
        **query_parameters
    )
    return MaintenanceLogsResponse(maintenance_logs=maintenance_logs)
