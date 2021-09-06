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

@server.on("close")
async def on_close(client, code, reason):
    print(f"Client at {client.remote_address} closed connection with code: {code} and reason: {reason}")

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

@client.on("close")
async def on_close(code, reason):
    print(f"{client.connection.remote_address} closed connection with code: {code} and reason: {reason}")

client.connect("ws://localhost:3000")
```

## FAQ
### What's the difference between `on_disconnect` and `on_close` event listeners ?
The difference isn't huge but it is there. `on_disconnect` event is fired only if the client or the server **did not** closed the connection properly, the TCP Connection was lost suddenly raising the websockets' ConnectionClosedError in the libraries internal message consumer. In such cases the code returned is usually `1006` and there is no reason. While `on_close` event listener is called if the connection was closed properly, that could be done by calling the libraries' ClientSocket or ServerSocket's `.close` method and providing a reason and error code optionally. This causes the internal message consumer task on both sides to exit / return that in turn calls the attached listener functions. 
**Note:** Unlike `on_disconnect` listener, `on_close` is called on both sides that is both on the client and server websocket sides with the same reason and code.
### Why this exists?
I made this library because I was fed up of websockets library because it didn't have event based communication like Node.js's ws library and that made it difficult to work about it. Before I was doubtful whether I would work on it anymore or not... but it has went on to become a pretty large library but still not well known as of now... 
