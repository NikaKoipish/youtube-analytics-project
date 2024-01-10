import json
from googleapiclient.discovery import build
import os

class Channel:
    """Класс для ютуб-канала"""
    API_KEY: str = os.getenv('API_YouTube')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.dict_to_print = self.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()

        dict_youtube = json.loads(json.dumps(self.dict_to_print, indent=2, ensure_ascii=False))
        self.title = dict_youtube["items"][0]["snippet"]["title"]
        self.description = dict_youtube["items"][0]["snippet"]["description"]
        self.subscriberCount = int(dict_youtube["items"][0]["statistics"]["subscriberCount"])
        self.video_count = dict_youtube["items"][0]["statistics"]["videoCount"]
        self.viewCount = dict_youtube["items"][0]["statistics"]["viewCount"]
        self.url = dict_youtube["items"][0]["snippet"]["thumbnails"]["default"]["url"]

    def to_json(self, file_name):
        data = {
            "id": self.__channel_id,
            "title": self.title,
            "description" : self.description,
            "url": self.url,
            "subscriberCount": self.subscriberCount,
            "video_count": self.video_count,
            "viewCount": self.viewCount
        }
        with open(file_name, 'w', encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel_data = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel_data, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.API_KEY)

    def __str__(self):
        return f"'{self.title}(https://www.youtube.com/channel/{self.__channel_id})'"

    def __add__(self, other):
        return self.subscriberCount + other.subscriberCount

    def __sub__(self, other):
        return self.subscriberCount - other.subscriberCount and other.subscriberCount - self.subscriberCount

    def __lt__(self, other):
        return self.subscriberCount < other.subscriberCount

    def __le__(self, other):
        return self.subscriberCount <= other.subscriberCount

    def __gt__(self, other):
        return self.subscriberCount > other.subscriberCount

    def __ge__(self, other):
        return self.subscriberCount >= other.subscriberCount



