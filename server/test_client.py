import asyncio
import json
import websockets

async def run():
    uri = "ws://localhost:8765"

    async with websockets.connect(uri) as ws:
        print("Connected to server.")

        msg = await ws.recv()
        print("Server:", msg)

        while True:
            cmd = input(
                "\nCommand (create | join <id> | start <id> | leave <id> | quit): "
            ).strip()

            if cmd == "quit":
                break

            elif cmd == "create":
                await ws.send(json.dumps({"action": "create_lobby"}))
            
            elif cmd.startswith("join "):
                _, lobby_id = cmd.split(" ", 1)
                await ws.send(json.dumps({"action": "join_lobby", "lobby_id": lobby_id}))
            
            elif cmd.startswith("start "):
                _, lobby_id = cmd.split(" ", 1)
                await ws.send(json.dumps({"action": "start_lobby", "lobby_id": lobby_id}))
            
            elif cmd.startswith("leave "):
                _, lobby_id = cmd.split(" ", 1)
                await ws.send(json.dumps({"action": "leave_lobby", "lobby_id": lobby_id}))
            else:
                print("Unknown")
                continue
            
            response = await ws.recv()
            print("Server:", response)

if __name__ == "__main__":
    asyncio.run(run())
