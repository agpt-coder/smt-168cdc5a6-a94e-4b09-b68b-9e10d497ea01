from datetime import date
from typing import Dict, List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class RecoveryLogsResponse(BaseModel):
    """
    Response model containing the list of logs associated with past data recovery attempts, showing details for audits.
    """

    logs: List[Dict]


async def getRecoveryLogs(
    start_date: Optional[date], end_date: Optional[date], status: Optional[str]
) -> RecoveryLogsResponse:
    """
    Retrieves logs related to past data recovery attempts. This includes details such as the date and time of each recovery, and the description
    of the recovery attempt. Filters for status are not applicable as 'MaintenanceLog' doesn't have a 'status' field. Useful for auditing and
    troubleshooting recovery operations.

    Args:
        start_date (Optional[date]): The starting date from which to retrieve the recovery logs. Format: YYYY-MM-DD
        end_date (Optional[date]): The ending date up to which to retrieve the recovery logs. Format: YYYY-MM-DD
        status (Optional[str]): This parameter is not used as 'MaintenanceLog' does not include 'status'.

    Returns:
        RecoveryLogsResponse: Response model containing the list of logs associated with past data recovery attempts, showing details for audits.
    """
    query_parameters = {}
    if start_date:
        query_parameters["date"] = {"gte": start_date}
    if end_date:
        if "date" in query_parameters:
            query_parameters["date"]["lte"] = end_date
        else:
            query_parameters["date"] = {"lte": end_date}
    logs = await prisma.models.MaintenanceLog.prisma().find_many(where=query_parameters)
    formatted_logs = [
        {"date": log.date, "description": log.description} for log in logs
    ]
    return RecoveryLogsResponse(logs=formatted_logs)
