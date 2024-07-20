# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir discord.py websockets aiohttp

# Make port 8765 and 8764 available to the world outside this container
EXPOSE 8765 8764

# Set environment variables with default values
ENV DISCORD_TOKEN=""
ENV CHANNEL_ID=""
ENV LOG_LEVEL="INFO"
ENV WEBHOOK_URL=""

# Run the script when the container launches
CMD ["python", "bot.py"]