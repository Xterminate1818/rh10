import asyncio
import websockets
import json

var = []

async def test():
    #websocket = await websockets.connect('ws://localhost:8080/bots')
    websocket = await websockets.connect('ws://192.168.0.20:8080/bots')

    await websocket.send(json.dumps({"throttle": 0.0, "steer": 0.0, "breaking": 0.0, "id":-1}))

    response = await websocket.recv()
    print(response)

    # try:
    #     await websocket.send(json.dumps({"throttle": 0.0, "steer": 0.0, "breaking": 0.0, "id":-1}))
    # finally:
    #     #await websocket.close()
    #     print("sent!")

asyncio.run(test())

print(var)


# import asyncio
# import websockets
# import json

# var = []

# async def test():
#     async with websockets.connect('ws://192.168.0.20:8080/bots') as websocket:
#         #response = await websocket.recv()
#         #print(response)

#         #await websocket.send("ping")
#         #response = await websocket.recv()
#         #print(response)
#         #var.append(response)

#         await websocket.send(json.dumps({"op": "subscribe", "args": "test"}))
#         #response = await websocket.recv()
#         #print(response)

# asyncio.get_event_loop().run_until_complete(test())

# print(var)