from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN

from directory.config import settings
from directory.database import get_db
from directory.repositories.repository import OrganizationRepository
from directory.services.service import OrganizationService

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

API_KEY = settings.API_KEY


async def get_api_key(api_key: Annotated[str, Depends(api_key_header)]):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Could not validate API key",
        )


def get_organisation_repository(
    db: Annotated[Session, Depends(get_db)]
) -> OrganizationRepository:
    return OrganizationRepository(db)


def get_service(
    org_rep: Annotated[OrganizationRepository, Depends(get_organisation_repository)],
) -> OrganizationService:
    return OrganizationService(org_rep)
