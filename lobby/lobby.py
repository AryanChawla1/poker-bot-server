import uuid

from lobby.client import Client


class Lobby:
    def __init__(self, host: Client, max_size: int = 5):
        self.lobby_id = str(uuid.uuid4())
        self.host = host
        self.max_size = max_size
        self.clients: dict[str, Client] = {host.user_id: host}
        self.is_active = False

    def add_client(self, client: Client) -> bool:
        if self.is_active:
            return False
        if len(self.clients) >= self.max_size:
            return False
        self.clients[client.user_id] = client
        return True

    def remove_client(self, user_id: str) -> bool:
        if user_id not in self.clients:
            return False

        del self.clients[user_id]

        if self.host.user_id == user_id and self.clients:
            self.host = next(iter(self.clients.values()))

        return True

    def start(self) -> bool:
        if self.is_active:
            return False
        self.is_active = True
        return True

    def is_empty(self) -> bool:
        return len(self.clients) == 0

    def list_clients(self):
        return list(self.clients.values())
