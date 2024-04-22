from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class BackupStatusRequest(BaseModel):
    """
    Request model for fetching the current status of the data backup process. This endpoint does not require any input parameters.
    """

    pass


class BackupStatusResponse(BaseModel):
    """
    Provides detailed information about the current status of the data backup process, including progress, operational status, and error messages if any.
    """

    progress: int
    status: str
    errorMessage: Optional[str] = None


async def getBackupStatus(request: BackupStatusRequest) -> BackupStatusResponse:
    """
    Provides the current status of the last initiated backup process. Useful for monitoring ongoing backups or verifying the state of the last backup task. The output includes the progress percentage, current status (e.g., in progress, completed, error), and any relevant error messages if the backup failed.

    Args:
        request (BackupStatusRequest): Request model for fetching the current status of the data backup process. This endpoint does not require any input parameters.

    Returns:
        BackupStatusResponse: Provides detailed information about the current status of the data backup process, including progress, operational status, and error messages if any.
    """
    latest_production_record = await prisma.models.ProductionRecord.prisma().find_first(
        order={"createdAt": "desc"}
    )
    if not latest_production_record:
        return BackupStatusResponse(
            progress=0, status="No backup available", errorMessage=None
        )
    from datetime import datetime, timedelta

    now = datetime.now()
    latest_update = latest_production_record.createdAt.replace(tzinfo=None)
    if now - latest_update > timedelta(days=1):
        status = "error"
        progress = 100
        error_message = "Backup took too long, check system"
    elif now - latest_update > timedelta(hours=1):
        status = "in progress"
        progress = int((now - latest_update).seconds / 3600 * 100)
        error_message = None
    else:
        status = "completed"
        progress = 100
        error_message = None
    return BackupStatusResponse(
        progress=progress, status=status, errorMessage=error_message
    )
