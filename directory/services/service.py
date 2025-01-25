from directory.models import Building, Organization
from directory.repositories.repository import OrganizationRepository


class OrganizationService:
    def __init__(self, org_rep: OrganizationRepository):
        self._organization_repository = org_rep

    def get_organizations_by_building(self, building_id: int) -> list[Organization]:
        return self._organization_repository.get_organizations_by_building(building_id)

    def get_organizations_by_activity(self, activity_id: int) -> list[Organization]:
        return self._organization_repository.get_organizations_by_activity(activity_id)

    def get_organizations_in_radius(
        self, lat: float, lon: float, radius: float
    ) -> list[Organization]:
        return self._organization_repository.get_organizations_in_radius(
            lat, lon, radius
        )

    def get_buildings(self) -> list[Building]:
        return self._organization_repository.get_buildings()

    def get_organization_by_id(self, organization_id: int) -> Organization:
        return self._organization_repository.get_organization_by_id(organization_id)

    def search_organizations_by_activity_tree(
        self, root_activity_id: int
    ) -> list[Organization]:
        return self._organization_repository.search_organizations_by_activity_tree(
            root_activity_id
        )

    def search_organizations_by_name(self, name: str) -> list[Organization]:
        return self._organization_repository.search_organizations_by_name(name)
