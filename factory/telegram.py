import uuid

from telethon import TelegramClient

from config.constants import Constants

def telegram_client(session_name = uuid.uuid4().hex):
    client = TelegramClient(session_name, Constants.API_ID, Constants.API_HASH)
    return client