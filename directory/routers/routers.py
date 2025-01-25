from typing import Annotated

from fastapi import APIRouter, Depends

from directory.dependencies import get_service
from directory.schemas import BuildingBase, OrganizationBase
from directory.services.service import OrganizationService

router = APIRouter()


@router.get(
    "/organizations/building/{building_id}", response_model=list[OrganizationBase]
)
def get_organizations_by_building(
    building_id: int, service: Annotated[OrganizationService, Depends(get_service)]
):
    return service.get_organizations_by_building(building_id)


@router.get(
    "/organizations/activity/{activity_id}", response_model=list[OrganizationBase]
)
def get_organizations_by_activity(
    activity_id: int, service: Annotated[OrganizationService, Depends(get_service)]
):
    return service.get_organizations_by_activity(activity_id)


@router.get("/organizations/radius", response_model=list[OrganizationBase])
def get_organizations_in_radius(
    lat: float,
    lon: float,
    radius: float,
    service: Annotated[OrganizationService, Depends(get_service)],
):
    return service.get_organizations_in_radius(lat, lon, radius)


@router.get("/buildings", response_model=list[BuildingBase])
def get_buildings(service: Annotated[OrganizationService, Depends(get_service)]):
    return service.get_buildings()


@router.get("/organization/{organization_id}", response_model=OrganizationBase)
def get_organization_by_id(
    organization_id: int, service: Annotated[OrganizationService, Depends(get_service)]
):
    return service.get_organization_by_id(organization_id)


@router.get("/organizations/search/tree", response_model=list[OrganizationBase])
def search_organizations_by_activity_tree(
    root_activity_id: int, service: Annotated[OrganizationService, Depends(get_service)]
):
    return service.search_organizations_by_activity_tree(root_activity_id)


@router.get("/organizations/search", response_model=list[OrganizationBase])
def search_organizations_by_name(
    name: str, service: Annotated[OrganizationService, Depends(get_service)]
):
    return service.search_organizations_by_name(name)
