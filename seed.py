from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from directory.config import settings
from directory.models import Activity, Base, Building, Organization

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)


def seed_data():
    session = SessionLocal()
    try:
        session.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(text(f"TRUNCATE TABLE {table.name};"))
        session.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
        session.commit()

        building1 = Building(
            address="г. Москва, ул. Ленина 1", latitude=55.7558, longitude=37.6173
        )
        building2 = Building(
            address="г. Санкт-Петербург, Невский проспект 32",
            latitude=59.9343,
            longitude=30.3351,
        )

        activity_food = Activity(name="Еда")
        activity_meat = Activity(name="Мясная продукция", parent=activity_food)
        activity_meat_cow = Activity(name="Мясо коров", parent=activity_meat)
        activity_milk = Activity(name="Молочная продукция", parent=activity_food)

        activity_cars = Activity(name="Автомобили")
        activity_parts = Activity(name="Запчасти", parent=activity_cars)

        organization1 = Organization(
            name="ООО 'Рога и Копыта'",
            phone_numbers="2-222-222, 3-333-333",
            building=building1,
            activities=[activity_food, activity_meat, activity_meat_cow],
        )
        organization2 = Organization(
            name="ООО 'Молочная Ферма'",
            phone_numbers="8-923-666-13-13",
            building=building2,
            activities=[activity_food, activity_milk],
        )
        organization3 = Organization(
            name="ООО 'Автозапчасти'",
            phone_numbers="8-923-236-45-03",
            building=building2,
            activities=[activity_cars, activity_parts],
        )
        session.add_all(
            [
                building1,
                building2,
                activity_food,
                activity_meat,
                activity_milk,
                activity_cars,
                activity_parts,
                organization1,
                organization2,
                organization3,
                activity_meat_cow,
                activity_parts,
            ]
        )

        session.commit()
        print("Данные успешно загружены в базу!")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Ошибка при заполнении базы: {e}")
    finally:
        session.close()


def main():
    if settings.ENV != "development":
        print("Тестовые данные можно добавлять только в окружении разработки!")
        exit(1)
    Base.metadata.create_all(bind=engine)
    print("Таблицы созданы.")
    seed_data()


if __name__ == "__main__":
    main()
