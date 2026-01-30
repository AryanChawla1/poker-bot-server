from typing import Any

from server.logger import logger

class ConnectionManager:
    def __init__(self) -> None:
        self.connections: dict[str, Any] = {}

    def add(self, user_id: str, websocket: Any) -> None:
        logger.info(f'Added user: {user_id}')
        self.connections[user_id] = websocket

    def remove(self, user_id: str) -> None:
        logger.info(f'Removed user: {user_id}')
        self.connections.pop(user_id, None)

    def get(self, user_id: str) -> Any:
        return self.connections.get(user_id)

    async def send_to(self, user_id: str, message: dict) -> None:
        ws = self.get(user_id)
        if ws:
            logger.info(f"Sent user {user_id} message: {message}")
            await ws.send(message)
