from typing import Dict, List

from app.core.config import settings


class RouteConfig:
    def __init__(self, module_path: str, prefix: str, tags: List[str]):
        self.module_path = module_path
        self.prefix = prefix
        self.tags = tags


CLIENT_ROUTES = [
    RouteConfig("app.api.client.v1.auth", f"{settings.API_V1_STR}/auth", ["client-auth"]),
    RouteConfig("app.api.client.v1.user", f"{settings.API_V1_STR}/users", ["client-user"]),
    RouteConfig("app.api.client.v1.config", f"{settings.API_V1_STR}/config", ["client-config"]),
    RouteConfig("app.api.client.v1.department", f"{settings.API_V1_STR}/departments", ["client-department"]),
    RouteConfig("app.api.client.v1.doctor", f"{settings.API_V1_STR}/doctors", ["client-doctor"]),
    RouteConfig("app.api.client.v1.appointment", f"{settings.API_V1_STR}/appointments", ["client-appointment"]),
]

BACKOFFICE_ROUTES = []
COMMON_ROUTES = []


def register_routes(app, route_configs: List[RouteConfig]):
    for route_config in route_configs:
        module_name = route_config.module_path.rsplit(".", 1)[-1]
        module = __import__(route_config.module_path, fromlist=[module_name])
        app.include_router(
            module.router, prefix=route_config.prefix, tags=route_config.tags
        )


def get_client_routes() -> List[RouteConfig]:
    return CLIENT_ROUTES


def get_backoffice_routes() -> List[RouteConfig]:
    return BACKOFFICE_ROUTES


def get_common_routes() -> List[RouteConfig]:
    return COMMON_ROUTES


def get_all_routes() -> Dict[str, List[RouteConfig]]:
    return {
        "client": CLIENT_ROUTES,
        "backoffice": BACKOFFICE_ROUTES,
        "common": COMMON_ROUTES,
    }
