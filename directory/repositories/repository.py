from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from directory.models import Activity, Building, Organization


class OrganizationRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_organizations_by_building(self, building_id: int) -> list[Organization]:
        return self._session.scalars(
            select(Organization).where(Organization.building_id == building_id)
        ).all()

    def get_organizations_by_activity(self, activity_id: int) -> list[Organization]:
        return self._session.scalars(
            select(Organization)
            .join(Organization.activities)
            .where(Activity.id == activity_id)
        ).all()

    def get_organizations_in_radius(
        self, lat: float, lon: float, radius: float
    ) -> list[Organization]:
        distance_formula = func.sqrt(
            func.pow(Building.latitude - lat, 2) + func.pow(Building.longitude - lon, 2)
        )
        return self._session.scalars(
            select(Organization)
            .join(Organization.building)
            .where(distance_formula <= radius)
        ).all()

    def get_buildings(self) -> list[Building]:
        return self._session.scalars(select(Building)).all()

    def get_organization_by_id(self, organization_id: int) -> Organization:
        return self._session.scalar(
            select(Organization).where(Organization.id == organization_id)
        )

    def search_organizations_by_activity_tree(self, root_activity_id: int):
        main_ids = set()

        def get_descendant_ids(activity_id):
            nonlocal main_ids
            descendants = self._session.scalars(
                select(Activity.id).where(Activity.parent_id == activity_id)
            ).all()
            print("descendants", descendants)
            ids = set(descendants)
            print("ids-set", ids)
            for descendant in descendants:
                print("descendant", descendant)
                main_ids.add(descendant)
                main_ids.update(get_descendant_ids(descendant))
                print("main_ids", main_ids)
                print("ids2", ids)
            print("ids3", ids)
            return main_ids

        activity_ids = {root_activity_id, *get_descendant_ids(root_activity_id)}
        print("activity_ids", activity_ids)
        return self._session.scalars(
            select(Organization)
            .distinct()
            .join(Organization.activities)
            .where(Activity.id.in_(activity_ids))
        ).all()

    def search_organizations_by_name(self, name: str) -> Organization:
        return self._session.scalars(
            select(Organization).where(Organization.name.ilike(f"%{name}%"))
        ).all()
