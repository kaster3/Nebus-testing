import asyncio
import json
import sys
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.database.db_helper import db_helper
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


async def main() -> None:
    async for session in db_helper.session_getter():
        await load_fixtures(session)


if __name__ == "__main__":
    asyncio.run(main())

