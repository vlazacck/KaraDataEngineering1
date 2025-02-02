
from telethon import TelegramClient
import os
import logging
from dotenv import load_dotenv
import psycopg2
import asyncio
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="telegram_scraping.log"
)

# Telegram API credentials
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

# PostgreSQL credentials
db_config = {
    "dbname": os.getenv("DB_NAME", "ethiopian_medical_data"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432")
}

# Telegram channels to scrape with their respective limits
channel_limits = {
    "DoctorsET": 100,
    "CheMed123": 50,
    "lobelia4cosmetics": 75,
    "yetenaweg": 100,
    "EAHCI": 60
}

# Initialize Telegram client
client = TelegramClient('user_session', api_id, api_hash)

def insert_message(channel_link, message):
    """
    Insert scraped message into PostgreSQL.
    """
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        media_link = None
        media_type = None
        if message.photo:
            media_link = f"https://t.me/{channel_link}/{message.id}"
            media_type = 'photo'
        elif message.document and hasattr(message.document, 'mime_type') and message.document.mime_type.startswith('image/'):
            media_link = f"https://t.me/{channel_link}/{message.id}"
            media_type = 'image_document'
        
        cursor.execute('''
            INSERT INTO raw_telegram_data (
                channel_name, message_id, message_text, media_link, media_type, timestamp
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (channel_name, message_id) DO NOTHING;
        ''', (
            channel_link,
            message.id,
            message.text,
            media_link,
            media_type,
            message.date
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logging.error(f"Error inserting message into PostgreSQL: {e}")

async def download_media(message, channel_link):
    """
    Download media files asynchronously.
    """
    if isinstance(message.media, MessageMediaPhoto):
        file_path = f"images/{channel_link}_{message.id}.jpg"
        try:
            await message.download_media(file=file_path)
            logging.info(f"Downloaded media: {file_path}")
        except Exception as e:
            logging.error(f"Error downloading media for message {message.id}: {e}")
    elif isinstance(message.media, MessageMediaDocument):
        # Check if the document is an image by its MIME type
        mime_type = message.media.document.mime_type if hasattr(message.media.document, 'mime_type') else None
        if mime_type and mime_type.startswith('image/'):
            file_path = f"images/{channel_link}_{message.id}.jpg"
            try:
                await message.download_media(file=file_path)
                logging.info(f"Downloaded media: {file_path}")
            except Exception as e:
                logging.error(f"Error downloading media for message {message.id}: {e}")

async def scrape_channel(channel_username, message_limit):
    """
    Scrape messages from a Telegram channel with a specified limit.
    """
    try:
        logging.info(f"Scraping data from channel: {channel_username} (Limit: {message_limit})")
        channel = await client.get_entity(channel_username)
        messages = await client.get_messages(channel, limit=message_limit)
        tasks = []
        for message in messages:
            print(f"Message ID: {message.id}, Text: {message.text}")  # Debug statement
            logging.info(f"Message ID: {message.id}, Text: {message.text}")
            insert_message(channel_username, message)
            if message.photo or (isinstance(message.media, MessageMediaDocument) and 
                                 hasattr(message.media.document, 'mime_type') and 
                                 message.media.document.mime_type.startswith('image/')):
                tasks.append(download_media(message, channel_username))
            await asyncio.sleep(0.1)  # Reduce delay to speed up processing
        
        # Run all download tasks concurrently
        await asyncio.gather(*tasks)
    except Exception as e:
        logging.error(f"Error scraping channel {channel_username}: {e}")

async def main():
    """
    Main function to scrape all channels.
    """
    await client.start()
    logging.info("User Client Created")
    for channel, limit in channel_limits.items():
        await scrape_channel(channel, limit)

# Ensure the images directory exists
os.makedirs('images', exist_ok=True)

# Run the script

from telethon import TelegramClient
import os
import logging
from dotenv import load_dotenv
import psycopg2
import asyncio
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="telegram_scraping.log"
)

# Telegram API credentials
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

# PostgreSQL credentials
db_config = {
    "dbname": os.getenv("DB_NAME", "ethiopian_medical_data"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432")
}

# Telegram channels to scrape with their respective limits
channel_limits = {
    "DoctorsET": 100,
    "CheMed123": 50,
    "lobelia4cosmetics": 75,
    "yetenaweg": 100,
    "EAHCI": 60
}

# Initialize Telegram client
client = TelegramClient('user_session', api_id, api_hash)

def insert_message(channel_link, message):
    """
    Insert scraped message into PostgreSQL.
    """
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        media_link = None
        media_type = None
        if message.photo:
            media_link = f"https://t.me/{channel_link}/{message.id}"
            media_type = 'photo'
        elif message.document and hasattr(message.document, 'mime_type') and message.document.mime_type.startswith('image/'):
            media_link = f"https://t.me/{channel_link}/{message.id}"
            media_type = 'image_document'
        
        cursor.execute('''
            INSERT INTO raw_telegram_data (
                channel_name, message_id, message_text, media_link, media_type, timestamp
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (channel_name, message_id) DO NOTHING;
        ''', (
            channel_link,
            message.id,
            message.text,
            media_link,
            media_type,
            message.date
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logging.error(f"Error inserting message into PostgreSQL: {e}")

async def download_media(message, channel_link):
    """
    Download media files asynchronously.
    """
    if isinstance(message.media, MessageMediaPhoto):
        file_path = f"images/{channel_link}_{message.id}.jpg"
        try:
            await message.download_media(file=file_path)
            logging.info(f"Downloaded media: {file_path}")
        except Exception as e:
            logging.error(f"Error downloading media for message {message.id}: {e}")
    elif isinstance(message.media, MessageMediaDocument):
        # Check if the document is an image by its MIME type
        mime_type = message.media.document.mime_type if hasattr(message.media.document, 'mime_type') else None
        if mime_type and mime_type.startswith('image/'):
            file_path = f"images/{channel_link}_{message.id}.jpg"
            try:
                await message.download_media(file=file_path)
                logging.info(f"Downloaded media: {file_path}")
            except Exception as e:
                logging.error(f"Error downloading media for message {message.id}: {e}")

async def scrape_channel(channel_username, message_limit):
    """
    Scrape messages from a Telegram channel with a specified limit.
    """
    try:
        logging.info(f"Scraping data from channel: {channel_username} (Limit: {message_limit})")
        channel = await client.get_entity(channel_username)
        messages = await client.get_messages(channel, limit=message_limit)
        tasks = []
        for message in messages:
            print(f"Message ID: {message.id}, Text: {message.text}")  # Debug statement
            logging.info(f"Message ID: {message.id}, Text: {message.text}")
            insert_message(channel_username, message)
            if message.photo or (isinstance(message.media, MessageMediaDocument) and 
                                 hasattr(message.media.document, 'mime_type') and 
                                 message.media.document.mime_type.startswith('image/')):
                tasks.append(download_media(message, channel_username))
            await asyncio.sleep(0.1)  # Reduce delay to speed up processing
        
        # Run all download tasks concurrently
        await asyncio.gather(*tasks)
    except Exception as e:
        logging.error(f"Error scraping channel {channel_username}: {e}")

async def main():
    """
    Main function to scrape all channels.
    """
    await client.start()
    logging.info("User Client Created")
    for channel, limit in channel_limits.items():
        await scrape_channel(channel, limit)

# Ensure the images directory exists
os.makedirs('images', exist_ok=True)

# Run the script
with client:

    client.loop.run_until_complete(main())