import asyncio
import websockets
import json

sender = input('Enter username: ')
txt = input('Entet message: ')
to = input('Enter recipient name: ')

message = {
    'sender': sender,
    'txt': txt,
    'to': to
}

async def hello(msg_obj):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        
        parsed = json.dumps(msg_obj)
        
        await websocket.send(parsed)
        print(f">>> {msg_obj}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")

if __name__ == "__main__":
    asyncio.run(hello(message))