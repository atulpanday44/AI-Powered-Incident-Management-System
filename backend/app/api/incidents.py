"""
FastAPI routes for incident management.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.db import get_db
from app.schemas import (
    IncidentCreate,
    IncidentResponse,
    IncidentUpdate,
)
from app.services import IncidentService
from datetime import datetime

router = APIRouter(prefix="/api/v1", tags=["incidents"])


@router.post("/incidents", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED)
async def create_incident(
    incident_request: IncidentCreate,
    db: Session = Depends(get_db),
) -> IncidentResponse:
    """
    Create new incident.

    Args:
        incident_request: Incident data
        db: Database session

    Returns:
        Created incident

    Raises:
        HTTPException: If creation fails
    """
    try:
        incident_data = {
            "title": incident_request.title,
            "service": incident_request.service,
            "severity": incident_request.severity.value,
            "cluster_id": incident_request.cluster_id,
            "anomaly_score": incident_request.anomaly_score,
        }

        incident = IncidentService.create_incident(db, incident_data)
        if not incident:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create incident"
            )

        return IncidentResponse.model_validate(incident)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create incident: {str(e)}"
        )


@router.get("/incidents", response_model=List[IncidentResponse])
async def get_incidents(
    service: Optional[str] = None,
    status_filter: Optional[str] = None,
    severity: Optional[str] = None,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[IncidentResponse]:
    """
    Retrieve incidents with optional filtering.

    Args:
        service: Filter by service name
        status_filter: Filter by status
        severity: Filter by severity
        limit: Maximum number of incidents
        db: Database session

    Returns:
        List of incidents
    """
    try:
        incidents = IncidentService.get_incidents(
            db,
            service=service,
            status=status_filter,
            severity=severity,
            limit=limit
        )
        return [IncidentResponse.model_validate(incident) for incident in incidents]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve incidents: {str(e)}"
        )


@router.get("/incidents/{incident_id}", response_model=IncidentResponse)
async def get_incident(
    incident_id: UUID,
    db: Session = Depends(get_db),
) -> IncidentResponse:
    """
    Get specific incident by ID.

    Args:
        incident_id: Incident ID
        db: Database session

    Returns:
        Incident object

    Raises:
        HTTPException: If incident not found
    """
    try:
        incident = IncidentService.get_incident_by_id(db, incident_id)
        if not incident:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Incident {incident_id} not found"
            )
        return IncidentResponse.model_validate(incident)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve incident: {str(e)}"
        )


@router.patch("/incidents/{incident_id}", response_model=IncidentResponse)
async def update_incident(
    incident_id: UUID,
    incident_update: IncidentUpdate,
    db: Session = Depends(get_db),
) -> IncidentResponse:
    """
    Update incident.

    Args:
        incident_id: Incident ID to update
        incident_update: Update data
        db: Database session

    Returns:
        Updated incident

    Raises:
        HTTPException: If incident not found or update fails
    """
    try:
        update_data = {}
        if incident_update.status:
            update_data["status"] = incident_update.status.value
        if incident_update.severity:
            update_data["severity"] = incident_update.severity.value

        incident = IncidentService.update_incident(db, incident_id, update_data)
        if not incident:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Incident {incident_id} not found"
            )
        return IncidentResponse.model_validate(incident)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update incident: {str(e)}"
        )


@router.get("/incidents-summary", response_model=dict)
async def get_incidents_summary(db: Session = Depends(get_db)) -> dict:
    """
    Get incident statistics and summary.

    Args:
        db: Database session

    Returns:
        Statistics dictionary
    """
    try:
        stats = IncidentService.get_statistics(db)
        return {
            **stats,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get statistics: {str(e)}"
        )
