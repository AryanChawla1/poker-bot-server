
from lobby.client import Client
from lobby.lobby import Lobby


class LobbyManager:
    def __init__(self):
        self.lobbies: dict[str, Lobby] = {}

    def create_lobby(self, host: Client, max_size: int = 5) -> Lobby:
        lobby = Lobby(host, max_size)
        self.lobbies[lobby.lobby_id] = lobby
        return lobby

    def get_lobby(self, lobby_id: str) -> Lobby | None:
        return self.lobbies.get(lobby_id)

    def join_lobby(self, lobby_id: str, client: Client) -> bool:
        lobby = self.get_lobby(lobby_id)
        if not lobby:
            return False

        return lobby.add_client(client)

    def leave_lobby(self, lobby_id: str, user_id: str) -> bool:
        lobby = self.get_lobby(lobby_id)
        if not lobby:
            return False

        lobby.remove_client(user_id)

        if lobby.is_empty():
            del self.lobbies[lobby_id]

        return True

    def list_lobbies(self):
        return list(self.lobbies.values())


if __name__ == "__main__":
    manager = LobbyManager()
    alice = Client("1", "Alice")
    bob = Client("2", "Bob")
    charlie = Client("3", "Charlie")

    lobby = manager.create_lobby(alice, max_size=4)
    print("Lobby created:", lobby.lobby_id)

    manager.join_lobby(lobby.lobby_id, bob)
    manager.join_lobby(lobby.lobby_id, charlie)

    print("Clients in lobby:", lobby.list_clients())

    lobby.start()
    print("Lobby active:", lobby.is_active)

    manager.leave_lobby(lobby.lobby_id, alice.user_id)
    print("After Alice leaves:", lobby.list_clients())
