# ws
WebSocket implementation in Python built on top of websockets python library. Similar to Node.js's ws.

Basic usage.

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

Event collector (.wait_for method) example.

`server.py`
```py
import ws
import asyncio

server = ws.ServerSocket()

@server.on('ready')
async def on_ready():
    print(f"Server is ready listening at ws://{server.address}:{server.port}")

@server.on('connect')
async def on_connect(websocket, path):
    print(f"Client at {websocket.remote_address} connected.")

@server.on('message')
async def on_message(message):
    print(f"{message.data}")
    if message.data.startswith("!confirm"):
        await message.author.send("Send yes or no?")
        try:
            conmes = await server.wait_for(
                'message', 
                timeout=300, 
                check=lambda rm: rm.data.lower().strip() in ['yes', 'no'] and rm.author.remote_address == message.author.remote_address)
            print(conmes.data)
            if conmes.data.lower().strip() == 'yes':
                await conmes.author.send("done")
            else:
                await conmes.author.send("not done")
        except asyncio.TimeoutError:
            await message.author.send("Timed out!")

@server.on('disconnect')
async def on_disconnect(client, code, reason):
    print(f"{client} disconnect with code:", code, reason)
    print(server.disconnected_clients)

@server.on("close")
async def on_close(client, code, reason):
    print(f"{client.remote_address} closed connection with code: {code} and reason: {reason}")

server.listen("localhost", 3000)
```

`client.py`
```py
import ws
import asyncio

client = ws.ClientSocket()

@client.on('connect')
async def on_connect():
    print(f"Connected to {client.connection.remote_address}")
    await client.send(content="!confirm")

@client.on('message')
async def on_message(message):
    print(f'{message.data}')
    if message.data in ['done', 'not done']:
        return
    await asyncio.sleep(3)
    await message.author.send(
         "This is a random message. This won't be collected by the event collector on the server side due to the check condition."
    )
    await asyncio.sleep(3)
    await message.author.send(
        "yes"
    ) #this will be collected and you would receive a response "done" for this, provide "no" and you will get "not done" response

@client.on('disconnect')
async def on_disconnect(code, reason):
    print(f"{client.connection} disconnect with code:", code, reason)
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
