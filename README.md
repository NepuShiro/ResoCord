# Resonite Companion Item and Discord Bot

This project consists of a companion item for the game Resonite and a Discord bot that facilitates communication between the game and a Discord channel. The system allows players in Resonite to send messages to a Discord channel and vice versa.

## Resonite Companion Item

To use the companion item in Resonite:

1. Spawn the item using the following link in Resonite:
   ```
   NepuShiro's Public > Tools > ResoCord 1.0.0
   resrec:///U-NepuShiro/R-38b577c8-c87e-4584-aa5f-12020c931731
   ```

2. Once spawned, you need to configure the WebSocket URLs:
   - Inspect the item in Resonite
   - Navigate to: `ItemRoot/Handling/ResDiscord Bridge/Websockets`
   - Locate the WebSocket URL fields and update them to match your Discord bot's WebSocket server address

   Note: The exact WebSocket URLs will depend on where you're hosting your Discord bot. If you're running the bot on the same machine as Resonite, you might use `ws://localhost:8765` and `ws://localhost:8764`, but make sure to use the correct IP address or domain if the bot is hosted elsewhere.

3. After updating the WebSocket URLs, the item should be ready to use.

## Discord Bot Setup

### Prerequisites

- Docker installed on your system
- A Discord bot token
- A Discord channel ID
- A Discord webhook URL

### Setup Steps

1. Clone this repository to your local machine.

2. Build the Docker image:
   ```bash
   docker build -t resonite-discord-bot .
   ```

3. Run the Docker container with the required environment variables:
   ```bash
   docker run -p 8765:8765 -p 8764:8764 \
     -e DISCORD_TOKEN=your_discord_bot_token \
     -e CHANNEL_ID=your_discord_channel_id \
     -e WEBHOOK_URL=your_discord_webhook_url \
     -e LOG_LEVEL=INFO \
     resonite-discord-bot
   ```

   Replace `your_discord_bot_token`, `your_discord_channel_id`, and `your_discord_webhook_url` with your actual Discord bot token, channel ID, and webhook URL respectively.

### Environment Variables

- `DISCORD_TOKEN`: Your Discord bot token
- `CHANNEL_ID`: The ID of the Discord channel to send/receive messages
- `WEBHOOK_URL`: The Discord webhook URL for sending messages
- `LOG_LEVEL`: The logging level (e.g., INFO, DEBUG, WARNING)

## Usage

Once both the Resonite companion item and the Discord bot are set up:

1. Messages sent through the companion item in Resonite will appear in the specified Discord channel.
2. Messages sent in the specified Discord channel will be broadcasted to all connected Resonite clients with the companion item.

## Troubleshooting

- If messages are not being sent or received, check the Docker logs for any error messages:
  ```bash
  docker logs resonite-discord-bot
  ```

- Ensure that your Discord bot has the necessary permissions in the specified channel.
- Verify that the webhook URL is correct and active.
- Double-check that the WebSocket URLs in the Resonite companion item are correctly set and match your bot's hosting environment.

## Contributing

If you'd like to contribute to this project, please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or support, please open an issue in the repository.
