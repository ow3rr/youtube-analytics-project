import json
import requests
from googleapiclient.discovery import build
import os


response = requests.get('https://developers.google.com/youtube/v3/docs/channels/list')
API_KEY: str = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=API_KEY)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        self.channel_id = channel_id
        self.channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

    def print_info(self) -> None:
        channel_info = self.channel
        print(channel_info)
        """Выводит в консоль информацию о канале."""
