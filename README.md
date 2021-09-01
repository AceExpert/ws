# ws
WebSocket implementation in Python built on top of websockets python library. Similar to Node.js's ws.

### Under Development

Few examples for now.

`server.py`
```py
import ws

server = ws.ServerSocket()

@server.on('connect')
async def on_connect(websocket, path):
    print(f"Connected to {websocket.remote_address}")
    await websocket.send("hello bro")

@server.on('message')
async def on_message(message, websocket):
    print(f'Received message: "{message}" from {websocket.remote_address}')

server.listen("localhost", 3000)
```

`client.py`
```py
import ws

client = ws.ClientSocket("ws://localhost:3000")

@client.on('connect')
async def on_connect():
    print(f"Connected to {client.connection.remote_address}")

@client.on('message')
async def on_message(message):
    print(f'Received message: "{message}" from {client.connection.remote_address}')
    await client.send("huh")

client.connect()
```
## Why this exists?
I made this library because I was fed up of websockets library because it didn't have event based communication like Node.js's ws library and that made it difficult to work about it. I **may or may not** work on it any more, don't keep any expectations, this is a one day project lol. 
