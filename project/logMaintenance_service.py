from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class MaintenanceRecordResponse(BaseModel):
    """
    Provides confirmation and details of the logged maintenance activity.
    """

    success: bool
    message: str
    maintenance_log_id: str


async def logMaintenance(
    equipment_id: str,
    description: str,
    maintenance_date: datetime,
    next_due_date: datetime,
    user_id: str,
) -> MaintenanceRecordResponse:
    """
    Records maintenance activities and schedules future reminders. This endpoint captures equipment data and stores maintenance logs.

    Args:
        equipment_id (str): Identifier for the equipment undergoing maintenance.
        description (str): Detailed description of the maintenance activities carried out.
        maintenance_date (datetime): The exact date and time when the maintenance was performed.
        next_due_date (datetime): Scheduled date for the next maintenance check.
        user_id (str): Identification of the Maintenance Manager responsible for the log entry.

    Returns:
        MaintenanceRecordResponse: Provides confirmation and details of the logged maintenance activity.

    Example:
        user_id = "12345-67890"
        equipment_id = "eq-001"
        description = "Routine check and oil change."
        maintenance_date = datetime.now()
        next_due_date = datetime.now() + timedelta(days=90)
        response = await logMaintenance(equipment_id, description, maintenance_date, next_due_date, user_id)
        if response.success:
            print("Maintenance logged successfully")
        else:
            print("Failed to log maintenance")
    """
    try:
        new_log = await prisma.models.MaintenanceLog.prisma().create(
            data={
                "userId": user_id,
                "description": description,
                "date": maintenance_date,
                "nextDueDate": next_due_date,
            }
        )
        return MaintenanceRecordResponse(
            success=True,
            message="Maintenance logged successfully",
            maintenance_log_id=new_log.id,
        )
    except Exception as e:
        return MaintenanceRecordResponse(
            success=False,
            message=f"Failed to log maintenance: {str(e)}",
            maintenance_log_id="",
        )
