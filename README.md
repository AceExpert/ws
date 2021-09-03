# ws
WebSocket implementation in Python built on top of websockets python library. Similar to Node.js's ws.

### Under Development

Few examples for now.

`server.py`
```py
import ws

server = ws.ServerSocket()

@server.on('ready')
async def on_ready():
    print(f"Server is ready. Listening at ws://{server.address}:{server.port}")

@server.on('connect')
async def on_connect(client, path):
    print(f"WebSocket at {client.remote_address} connected.")
    await client.send(data={'nice': 'bello', 'yes':'huh'})

@server.on('message')
async def on_message(message):
    print(f"{message.data}")

server.listen("localhost", 3000)
```

`client.py`
```py
import ws

client = ws.ClientSocket()

@client.on('connect')
async def on_connect():
    print(f"Connected to {client.connection.remote_address}")

@client.on('message')
async def on_message(message):
    print(f'{message.data}')
    print(f'{message.data.nice} {message.data.yes}')

client.connect("ws://localhost:3000")
```
## Why this exists?
I made this library because I was fed up of websockets library because it didn't have event based communication like Node.js's ws library and that made it difficult to work about it. I **may or may not** work on it any more, don't keep any expectations, this is a one day project lol. 
