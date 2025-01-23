from sqlalchemy import Column, Float, ForeignKey, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


organization_activity_association = Table(
    "organization_activity",
    Base.metadata,
    Column("organization_id", ForeignKey("organizations.id"), primary_key=True),
    Column("activity_id", ForeignKey("activities.id"), primary_key=True),
)


class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    organizations: Mapped[list["Organization"]] = relationship(
        "Organization", back_populates="building"
    )


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("activities.id"))

    children: Mapped[list["Activity"]] = relationship(
        "Activity", back_populates="parent", cascade="all, delete"
    )
    parent: Mapped["Activity | None"] = relationship(
        "Activity", back_populates="children", remote_side="Activity.id"
    )

    organizations: Mapped[list["Organization"]] = relationship(
        "Organization",
        secondary=organization_activity_association,
        back_populates="activities",
    )


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_numbers: Mapped[str] = mapped_column(String(255), nullable=False)
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"))

    building: Mapped["Building"] = relationship(
        "Building", back_populates="organizations"
    )
    activities: Mapped[list["Activity"]] = relationship(
        "Activity",
        secondary=organization_activity_association,
        back_populates="organizations",
    )
