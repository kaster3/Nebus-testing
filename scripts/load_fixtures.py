import json
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from core import settings
from core.database.db_helper import DataBaseHelper
from core.database.models import (
    Activity,
    Organization,
    OrganizationActivityAssociation,
    PhoneNumber,
)
from core.database.models.buildings import Building


FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures"


async def load_fixtures(session: AsyncSession) -> None:
    fixtures = {
        "buildings.json": Building,
        "activities.json": Activity,
        "organizations.json": Organization,
        "phone_numbers.json": PhoneNumber,
        "organization_activity_association.json": OrganizationActivityAssociation,
    }

    for file_name, model in fixtures.items():
        file_path = FIXTURES_DIR / file_name
        with open(file_path, "r") as file:
            data = json.load(file)
            for item_data in data:
                item = model(**item_data)
                session.add(item)
        await session.commit()


if __name__ == "__main__":
    db_helper = DataBaseHelper(
        url=str(settings.db.url),
        echo=settings.db.echo,
        echo_pool=settings.db.echo_pool,
        pool_size=settings.db.pool_size,
        max_overflow=settings.db.max_overflow,
    )
