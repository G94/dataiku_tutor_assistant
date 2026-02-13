"""Application bootstrap for local execution with cloud-ready boundaries."""

from fastapi import FastAPI

from dataiku_tutor.api.routes import build_router
from dataiku_tutor.config.settings import Settings


def create_app(config_path: str = "dataiku_tutor/config/settings.yaml") -> FastAPI:
    """Compose dependencies and return FastAPI app instance."""
    settings = Settings(config_path)

    # Dependency wiring placeholders (to be manually implemented)
    tutor_service = None
    index_updater = None

    app = FastAPI(title=settings.section("app").get("name", "dataiku_tutor"))
    app.include_router(build_router(tutor_service=tutor_service, index_updater=index_updater))
    return app


app = create_app()
