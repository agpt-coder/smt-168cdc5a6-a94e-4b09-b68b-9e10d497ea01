import json
from datetime import datetime
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class Detail(BaseModel):
    """
    Detailed data structure for each entry in a report's detailed section.
    """

    metric: str
    value: float
    timestamp: datetime


class ReportData(BaseModel):
    """
    Model representing the data section of a report. This type is flexible and would be tailored based on the specific report requirements.
    """

    summary: str
    details: List[Detail]


class GetReportResponse(BaseModel):
    """
    Response model for representing different kinds of reports. The structure might vary slightly depending on the report type, but generally, it provides the necessary report data.
    """

    reportType: str
    reportData: ReportData


async def fetchReports(reportType: str) -> GetReportResponse:
    """
    Generates and displays specified reports like production volume or sales revenue based on the 'reportType' parameter.

    Args:
        reportType (str): Type of the report requested by the user. This can be 'productionVolume', 'salesRevenue', etc.

    Returns:
        GetReportResponse: A response model including the type of report and its detailed data.

    Usage:
        response = await fetchReports('salesRevenue')
        print(response)
    """
    latest_report = await prisma.models.Report.prisma().find_first(
        where={"type": reportType}, order={"createdAt": "desc"}
    )
    if not latest_report:
        return GetReportResponse(
            reportType=reportType,
            reportData=ReportData(
                summary=f"No reports found for {reportType}", details=[]
            ),
        )
    report_data = ReportData(
        summary=f"Latest {reportType} report",
        details=[
            Detail(
                metric=item["metric"],
                value=item["value"],
                timestamp=datetime.fromisoformat(item["timestamp"]),
            )
            for item in json.loads(latest_report.content)
        ],
    )
    return GetReportResponse(reportType=reportType, reportData=report_data)
