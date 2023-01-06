import asyncio, websockets, json, jwt
from db import session, User, Message, Chat, ChatMedia, Media, Contact

clients = set()

async def authCheck():
    pass

async def dispatcher(websocket):
    clients.add(websocket)
    try:
        res = await websocket.recv()
        parsed = json.loads(res)
                # for client in clients:
                    # if client != websocket:
                    # client.send(message)
        
        await websocket.send({res})
        print(websocket)
        print(parsed)
    except Exception as e:
        print(e)

async def main_call():
    async with websockets.serve(dispatcher, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main_call())