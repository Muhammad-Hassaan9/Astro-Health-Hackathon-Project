from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.database import SessionLocal
from app.dependencies import get_current_user
from app.crud.astronaut import get_astronaut_by_user_id
from app.services.websocket_service import manager

router = APIRouter(tags=["WebSocket"])

@router.websocket("/ws/health")
async def health_websocket(websocket: WebSocket):
    await websocket.accept()

    astronaut_id = None

    try:
        # First message must contain the access token.
        auth_message = await websocket.receive_json()

        if (
            not isinstance(auth_message, dict)
            or auth_message.get("type") != "authenticate"
            or not auth_message.get("access_token")
        ):
            await websocket.close(
                code=4401,
                reason="Authentication required.",
            )
            return

        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=auth_message["access_token"],
        )

        # Verify the access token through Supabase.
        try:
            current_user = await get_current_user(credentials)
        except HTTPException as exc:
            await websocket.close(
                code=4401 if exc.status_code == 401 else 1011,
                reason="Authentication failed.",
            )
            return

        # Find the authenticated user's astronaut profile.
        db = SessionLocal()

        try:
            astronaut = get_astronaut_by_user_id(
                db,
                current_user.id,
            )

            astronaut_id = astronaut.id if astronaut else None
        finally:
            db.close()

        if astronaut_id is None:
            await websocket.close(
                code=4404,
                reason="Astronaut profile not found.",
            )
            return

        await manager.connect(astronaut_id, websocket)

        await websocket.send_json({
            "type": "connected",
            "message": "WebSocket connection established.",
            "astronaut_id": str(astronaut_id),
        })

        # Keep the connection alive and handle ping messages.
        while True:
            message = await websocket.receive_json()

            if isinstance(message, dict) and message.get("type") == "ping":
                await websocket.send_json({
                    "type": "pong",
                })
            else:
                await websocket.send_json({
                    "type": "error",
                    "message": "Unsupported message type.",
                })

    except WebSocketDisconnect:
        pass

    finally:
        if astronaut_id is not None:
            manager.disconnect(astronaut_id, websocket)