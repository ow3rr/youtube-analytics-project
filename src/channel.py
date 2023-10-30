import json
import requests
from googleapiclient.discovery import build
import os

response = requests.get('https://developers.google.com/youtube/v3/docs/channels/list')
API_KEY: str = os.getenv('YOUTUBE_API_KEY')


class Channel:
    """Класс для ютуб-канала
    Модифицируйте конструктор `Channel`, чтобы после инициализации экземпляр имел следующие атрибуты,
    заполненные реальными данными канала:
    - id канала
    - название канала
    - описание канала
    - ссылка на канал
    - количество подписчиков
    - количество видео
    - общее количество просмотров"""

    def __init__(self, channel_id: str) -> None:
        self.channel_id = channel_id
        self.channel = self.get_chanel_data()
        self.id = self.channel['items'][0]['id']
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.id}"
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = int(self.channel['items'][0]['statistics']['videoCount'])
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    """Переделываем получение данных по ютубу из атрибута в функцию"""

    def get_chanel_data(self) -> dict:
        youtube = self.get_service()
        channel_data = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        return channel_data

    def print_info(self) -> None:
        channel_info = self.channel
        print(json.dumps(channel_info, indent=2))
        """Выводит в консоль информацию о канале."""

    """метод `to_json()`, сохраняющий в файл значения атрибутов экземпляра `Channel`"""

    def to_json(self, filename: str) -> None:
        channel_json_data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count

        }
        with open(filename, 'w') as file:
            json.dump(channel_json_data, file, indent=2)

    """класс-метод `get_service()`, возвращающий объект для работы с YouTube API"""

    def __str__(self):
        return f"'{self.title} ({self.url})'"

    def __add__(self, other):
        return self.video_count + other.video_count

    def __sub__(self, other):
        return self.video_count - other.video_count

    def __gt__(self, other):
        return self.video_count > other.video_count

    def __ge__(self, other):
        return self.video_count >= other.video_count

    def __lt__(self, other):
        return self.video_count < other.video_count

    def __le__(self, other):
        return self.video_count <= other.video_count

    def __eq__(self, other):
        return self.video_count == other.video_count

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=API_KEY)
