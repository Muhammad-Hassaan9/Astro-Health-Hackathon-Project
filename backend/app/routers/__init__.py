from app.routers.auth import router as auth_router
from app.routers.health import router as health_router
from app.routers.alerts import router as alerts_router
from app.routers.websocket import router as websocket_router
from app.routers.astronaut import router as astronaut_router
from app.routers.ai import router as ai_router

__all__ = [
    "auth_router",
    "health_router",
    "alerts_router",
    "websocket_router",
    "astronaut_router",
    "ai_router",
]