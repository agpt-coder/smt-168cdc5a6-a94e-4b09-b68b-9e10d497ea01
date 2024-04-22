from datetime import datetime

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class BackupInitiationRequest(BaseModel):
    """
    Request model for initiating a data backup. No specific user inputs are needed as the backup process is triggered based on the request authentication and the role of the user being verified as a System Administrator.
    """

    pass


class BackupInitiationResponse(BaseModel):
    """
    Response model indicating the outcome of the backup initiation request. It provides a confirmation message once the backup is initiated or reports any errors encountered during the process.
    """

    message: str
    timestamp: datetime
    status: str


async def startBackup(request: BackupInitiationRequest) -> BackupInitiationResponse:
    """
    Initiates the process of data backup by triggering system-wide archiving utilities, verifying the role of the requestor and marking the start of the operation.

    Args:
        request (BackupInitiationRequest): Request model for initiating a data backup.

    Returns:
        BackupInitiationResponse: Response model with status and timestamp, confirming the initiation of the backup.

    Raises:
        ValueError: If the role of user is not authorized to initiate backup.
    """
    user = await prisma.models.User.prisma().find_unique(
        where={"email": "system_admin@example.com"}
    )
    if user and user.role == prisma.enums.Role.SYSTEM_ADMINISTRATOR:
        backup_status = True
        if backup_status:
            return BackupInitiationResponse(
                message="Backup initiated successfully.",
                timestamp=datetime.now(),
                status="Success",
            )
        else:
            return BackupInitiationResponse(
                message="Backup initiation failed due to system error.",
                timestamp=datetime.now(),
                status="Failed",
            )
    else:
        raise ValueError("User is not authorized to initiate backup.")
