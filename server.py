import asyncio, websockets, json, jwt
from db import session, User, Message, Chat, ChatMedia, Media, Contact

clients = set()

async def register(websocket):
    try:
        await websocket.wait_closed()
    finally:
        clients.remove(websocket)


async def dispatcher():
    message = 'Hello, this is the rrsponse fron the server'
    while True:
        websockets.send(clients, message)

async def main_call():
    async with websockets.serve(register, "localhost", 8765):
        await dispatcher()  # run forever

if __name__ == "__main__":
    asyncio.run(main_call())