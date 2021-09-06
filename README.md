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
    print(f"Server is ready listening at ws://{server.address}:{server.port}")

@server.on('connect')
async def on_connect(client, path):
    print(f"Client at {client.remote_address} connected.")
    await client.send(
            data={'status':"Okay", "alive": True, "ping": 10.4}
        )

@server.on('message')
async def on_message(message):
    print(f"{message.data}")
    print(f"Received from: {message.author.remote_address} at {message.created_at}")

@server.on('disconnect')
async def on_disconnect(client, code, reason):
    print(f"Client at {client.remote_address} disconnected with code: ", code, "and reason: ", reason)
    print(server.disconnected_clients)

server.listen("localhost", 3000)
```

`client.py`
```py
import ws

client = ws.ClientSocket()

@client.on('connect')
async def on_connect():
    print(f"Connected to {client.connection.remote_address}")
    print(client.connection)

@client.on('message')
async def on_message(message):
    print(f'{message.data}')
    print(f'Status: {message.data.status} Alive: {message.data.alive} Ping: {message.data.ping}')
    print(f"Received from: {message.author.remote_address} at {message.created_at}")
    await message.author.send(content="Okay received.")

@client.on('disconnect')
async def on_disconnect(code, reason):
    print(f"{client.connection} disconnect with code: ", code, "and reason: ", reason)
    print(client.disconnection)

client.connect("ws://localhost:3000")
```

## Why this exists?
I made this library because I was fed up of websockets library because it didn't have event based communication like Node.js's ws library and that made it difficult to work about it. Before I was doubtful whether I would work on it anymore or not... but it has went on to become a pretty large library but still not well known as of now... 
