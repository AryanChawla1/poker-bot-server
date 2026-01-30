import json
from pydantic import ValidationError

from lobby.client import Client
from lobby.lobby_manager import LobbyManager
from server.connection_manager import ConnectionManager
from server.logger import logger
from server.schemas import CreateLobbyMessage, JoinLobbyMessage, StartLobbyMessage, LeaveLobbyMessage

class LobbyHandlers:
    def __init__(self, lobby_manager: LobbyManager, connections: ConnectionManager):
        self.lobby_manager = lobby_manager
        self.connections = connections
    
    async def handle(self, user_id: str, message: str):
        try:
            data = json.loads(message)
            action = data.get("action")
        except json.JSONDecodeError:
            await self.connections.send_to(user_id, json.dumps({
                "type": "error",
                "message": "Invalid JSON"
            }))
            return
        
        try:
            if action == "create_lobby":
                msg = CreateLobbyMessage(**data)
                await self.create_lobby(user_id, msg)
            elif action == "join_lobby":
                msg = JoinLobbyMessage(**data)
                await self.join_lobby(user_id, msg)
            elif action == "leave_lobby":
                msg = LeaveLobbyMessage(**data)
                await self.leave_lobby(user_id, msg)
            elif action == "start_lobby":
                msg = StartLobbyMessage(**data)
                await self.start_lobby(user_id, msg)
            else:
                raise ValueError("Unknown action")
        except (ValidationError, ValueError) as e:
            await self.connections.send_to(user_id, json.dumps({
                "type": "error",
                "message": str(e)
            }))
    
    async def create_lobby(self, user_id: str, data: CreateLobbyMessage):
        name = data.name or f"Lobby-{user_id[:4]}"
        client = Client(user_id, name)
        lobby = self.lobby_manager.create_lobby(client)
        logger.info(f"User {user_id} creating lobby {lobby.lobby_id}")
        await self.connections.send_to(user_id, json.dumps({
            "type": "lobby_created",
            "lobby_id": lobby.lobby_id
        }))
    
    async def join_lobby(self, user_id: str, data: JoinLobbyMessage):
        lobby_id = data.lobby_id
        name = data.name or f"Lobby-{user_id[:4]}"
        client = Client(user_id, name)

        success = self.lobby_manager.join_lobby(lobby_id, client)
        logger.info(f"User {user_id} joining lobby {lobby_id}, status: {success}")
        await self.connections.send_to(user_id, json.dumps({
            "type": "join_result",
            "success": success,
            "lobby_id": lobby_id
        }))
    
    async def leave_lobby(self, user_id: str, data: LeaveLobbyMessage):
        lobby_id = data.lobby_id
        self.lobby_manager.leave_lobby(lobby_id, user_id)
        logger.info(f"User {user_id} leaving lobby {lobby_id}")
        await self.connections.send_to(user_id, json.dumps({
            "type": "left_lobby",
            "lobby_id": lobby_id
        }))

    async def start_lobby(self, user_id: str, data: StartLobbyMessage):
        lobby_id = data.lobby_id
        lobby = self.lobby_manager.get_lobby(lobby_id)

        if not lobby:
            return
        
        if lobby.host.user_id != user_id:
            await self.connections.send_to(user_id, json.dumps({
                "type": "error",
                "message": "Only host can start the lobby"
            }))
            return

        started = lobby.start()
        logger.info(f"User {user_id} starting lobby {lobby_id}")
        await self.connections.send_to(user_id, json.dumps({
            "type": "lobby_started",
            "success": started,
            "lobby_id": lobby_id
        }))
