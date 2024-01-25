from googleapiclient.discovery import build
import os

class Video:

    API_KEY: str = os.getenv('API_YouTube')

    def __init__(self, video_id):
        try:
            self.video_id = video_id
            self.video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.video_id
                                               ).execute()
            self.video_title: str = self.video_response['items'][0]['snippet']['title']
            self.url = f"https://www.youtube.com/watch?v={self.video_response['items'][0]['id']}'"
            self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']
        except Exception:
            self.video_id = video_id
            self.video_title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return f'{self.video_title}'

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.API_KEY)

class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id



