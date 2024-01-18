import json
from googleapiclient.discovery import build
import os

class Video:
    API_KEY: str = os.getenv('API_YouTube')

    def __init__(self, video_id):
        self.video_id = video_id
        self.video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                           id=self.video_id
                                           ).execute()
        self.video_title: str = self.video_response['items'][0]['snippet']['title']
        self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']
        self.comment_count: int = self.video_response['items'][0]['statistics']['commentCount']

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.API_KEY)




