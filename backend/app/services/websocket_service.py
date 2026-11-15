from uuid import UUID

from fastapi import WebSocket

class ConnectionManager:
    """Manage active WebSocket connections for astronauts."""

    def __init__(self):
        self.active_connections: dict[UUID, list[WebSocket]] = {}

    async def connect(
        self,
        astronaut_id: UUID,
        websocket: WebSocket,
    ) -> None:
        self.active_connections.setdefault(
            astronaut_id, []
        ).append(websocket)

    def disconnect(
        self,
        astronaut_id: UUID,
        websocket: WebSocket,
    ) -> None:
        connections = self.active_connections.get(astronaut_id, [])

        if websocket in connections:
            connections.remove(websocket)

        if not connections:
            self.active_connections.pop(astronaut_id, None)

    async def broadcast_to_astronaut(
        self,
        astronaut_id: UUID,
        message: dict,
    ) -> None:
        connections = self.active_connections.get(astronaut_id, [])

        for connection in connections.copy():
            try:
                await connection.send_json(message)
            except Exception:
                self.disconnect(astronaut_id, connection)

    async def send_health_update(
        self,
        astronaut_id: UUID,
        health_data: dict,
    ) -> None:
        await self.broadcast_to_astronaut(
            astronaut_id,
            {
                "type": "health_update",
                "data": health_data,
            },
        )

    async def send_alert(
        self,
        astronaut_id: UUID,
        alert_data: dict,
    ) -> None:
        await self.broadcast_to_astronaut(
            astronaut_id,
            {
                "type": "new_alert",
                "data": alert_data,
            },
        )

# One shared connection manager for the application.
manager = ConnectionManager()