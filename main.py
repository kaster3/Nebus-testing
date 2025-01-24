import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api import router as api_router
from core import settings
from core.database.db_helper import db_helper
from core.database.models.base import Base
from scripts.load_fixtures import load_fixtures


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(
        level=logging.INFO,
        format=settings.logging.log_format,
    )
    try:
        async with db_helper.engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        async for session in db_helper.session_getter():
            await load_fixtures(session)
        logging.info("Application starts successfully!")
        yield
        logging.info("Application ends successfully!")
    finally:
        async with db_helper.engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)


application = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

application.include_router(
    router=api_router,
)

def main() -> None:
    uvicorn.run(
        app=settings.conf.app,
        host=settings.conf.host,
        port=settings.conf.port,
        workers=settings.conf.workers,
        reload=settings.conf.reload,
    )


if __name__ == "__main__":
    main()
