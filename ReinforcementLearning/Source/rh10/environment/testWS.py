import asyncio
import websockets
import json

var = []

async def test():
    async with websockets.connect('wss://192.168.0.20:8080/bots') as websocket:
        response = await websocket.recv()
        print(response)

        await websocket.send("ping")
        response = await websocket.recv()
        print(response)
        var.append(response)

        await websocket.send(json.dumps({"op": "subscribe", "args": "test"}))
        response = await websocket.recv()
        print(response)

asyncio.get_event_loop().run_until_complete(test())

print(var)