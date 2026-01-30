from pydantic import BaseModel
from typing import Literal, Optional

class BaseMessage(BaseModel):
    action: str

class CreateLobbyMessage(BaseMessage):
    action: Literal["create_lobby"]
    name: Optional[str] = None

class JoinLobbyMessage(BaseMessage):
    action: Literal["join_lobby"]
    lobby_id: str
    name: Optional[str] = None

class StartLobbyMessage(BaseMessage):
    action: Literal["start_lobby"]
    lobby_id: str

class LeaveLobbyMessage(BaseMessage):
    action: Literal["leave_lobby"]
    lobby_id: str
