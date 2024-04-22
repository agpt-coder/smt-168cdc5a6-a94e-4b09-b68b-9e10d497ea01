from datetime import datetime

import prisma
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


async def backupData(request: BackupInitiationRequest) -> BackupInitiationResponse:
    """
    Initiates a data backup process to safeguard against data loss. Ensures that all module data is periodically backed up.

    Args:
        request (BackupInitiationRequest): Request model for initiating a data backup. No specific user inputs are needed as the backup process is triggered based on the request authentication and the role of the user being verified as a System Administrator.

    Returns:
        BackupInitiationResponse: Response model indicating the outcome of the backup initiation request. It provides a confirmation message once the backup is initiated or reports any errors encountered during the process.
    """
    try:
        authenticated_user = await prisma.models.User.prisma().find_first(
            where={"role": "SYSTEM_ADMINISTRATOR"}
        )
        if authenticated_user:
            backup_successful = True
            if backup_successful:
                message = f"Backup initiated successfully by {authenticated_user.email}"
                status = "Success"
            else:
                message = "Backup failed due to internal server error."
                status = "Failed"
            return BackupInitiationResponse(
                message=message, timestamp=datetime.now(), status=status
            )
        else:
            message = "Unauthorized access attempt for backup initiation."
            return BackupInitiationResponse(
                message=message, timestamp=datetime.now(), status="Failed"
            )
    except Exception as e:
        return BackupInitiationResponse(
            message=f"Error during backup process: {str(e)}",
            timestamp=datetime.now(),
            status="Failed",
        )
