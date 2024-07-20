import discord
import asyncio
import websockets
import logging
import os
import aiohttp

# Get environment variables
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID', 0))  # Default to 0 if not set
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

# WebSocket server address and port
WEBSOCKET_SERVER_ADDRESS = '0.0.0.0'
WEBSOCKET_SERVER_PORT = 8765
WEBSOCKET_SERVER_SEND_PORT = 8764

# List to store WebSocket clients
clients = set()

# Base URL for converting ResDB links
RESDB_BASE_URL = "https://skyfrost-archive.ydms.workers.dev/assets/"

# Defines your intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message events

# Create a Discord client
client = discord.Client(intents=intents)

# Event triggered when the bot is ready
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Event triggered when a message is received
@client.event
async def on_message(message):
    if message.channel.id != CHANNEL_ID:
        return
    
    # Continue if webhook, Skip if Bot
    if message.webhook_id is not None:
        pass
    elif message.author.bot:
        return
    
    # Format the message
    username = message.author.name
    profile_image = message.author.display_avatar.url
    formatted_message = f"{message.content}|{username}|{profile_image}"
    logging.info(f'Sending message to WebSocket server: {formatted_message}')
    
    # Send the message to the WebSocket server
    try:
        async with websockets.connect(f'ws://{WEBSOCKET_SERVER_ADDRESS}:{WEBSOCKET_SERVER_PORT}') as websocket:
            await websocket.send(formatted_message)
            logging.info("Message sent to WebSocket server successfully.")
    except Exception as e:
        logging.error(f'Error connecting to WebSocket server: {e}')

# WebSocket server logic for receiving messages
async def websocket_server_receive(websocket, path):
    clients.add(websocket)
    try:
        async for message in websocket:
            # Broadcast the received message to all clients
            for client in list(clients):
                if client.open:
                    await client.send(message)
                else:
                    clients.remove(client)
    except Exception as e:
        logging.error(f'Error in websocket_server_receive: {e}')
    finally:
        clients.discard(websocket)

# Function to send a message to Discord using a webhook
async def send_to_discord_webhook(message, username, user_id, icon_url, world_name):
    if not WEBHOOK_URL:
        logging.error("Webhook URL is not set. Skipping message send.")
        return
    
    icon_url = icon_url.replace("resdb://", RESDB_BASE_URL).rsplit('.', 1)[0]
    webhook_payload = {
        "username": f"{username} ({user_id}) : {world_name}",
        "avatar_url": icon_url,
        "content": message
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(WEBHOOK_URL, json=webhook_payload) as response:
            if response.status != 204:
                logging.error(f'Failed to send message to webhook: {response.status} {await response.text()}')

# WebSocket server logic for sending messages
async def websocket_server_send(websocket, path):
    async for message in websocket:
        try:
            msg, username, user_id, icon_url, world_name = message.split('|', 4)
            await send_to_discord_webhook(msg, username, user_id, icon_url, world_name)
            print(f'Sent message to Discord channel: {message}')
        except ValueError as e:
            logging.error(f'Error parsing message: {e}')

# Runs the Discord bot and the WebSocket servers concurrently
async def main():
    receive_server = websockets.serve(websocket_server_receive, WEBSOCKET_SERVER_ADDRESS, WEBSOCKET_SERVER_PORT)
    send_server = websockets.serve(websocket_server_send, WEBSOCKET_SERVER_ADDRESS, WEBSOCKET_SERVER_SEND_PORT)

    await asyncio.gather(
        client.start(TOKEN),
        receive_server,
        send_server
    )

# Runs the main coroutine
if __name__ == "__main__":
    logging.basicConfig(level=getattr(logging, LOG_LEVEL.upper(), 'INFO'))
    asyncio.run(main())