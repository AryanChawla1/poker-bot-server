class Client:
    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name

    def __repr__(self):
        return f"Client(user_id={self.user_id}, name={self.name})"
