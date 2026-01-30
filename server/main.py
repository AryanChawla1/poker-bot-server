import asyncio
import websockets
import uuid

from lobby.lobby_manager import LobbyManager
from server.connection_manager import ConnectionManager
from server.handlers import LobbyHandlers

lobby_manager = LobbyManager()
connections = ConnectionManager()
handlers = LobbyHandlers(lobby_manager, connections)

async def handler(websocket):
    user_id = str(uuid.uuid4())
    connections.add(user_id, websocket)

    try:
        await websocket.send(
            f'{{"type": "connected", "user_id": "{user_id}"}}'
        )

        async for message in websocket:
            await handlers.handle(user_id, message)
    
    finally:
        connections.remove(user_id)

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Websocket server runing on ws://localhost:8765")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())