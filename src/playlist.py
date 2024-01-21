import isodate
from googleapiclient.discovery import build
import os
from datetime import timedelta

class PlayList:
    API_KEY: str = os.getenv('API_YouTube')

    def __init__(self, playlist_id, title=None):
        self.playlist_id = playlist_id
        self.title = title
        youtube = build('youtube', 'v3', developerKey=self.API_KEY)
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        self.playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
                                                       part='contentDetails, snippet',
                                                       ).execute()
        self.channel_id = self.playlist_videos["items"][0]["snippet"]["channelId"]
        self.playlists = youtube.playlists().list(channelId=self.channel_id,
                                             part='contentDetails,snippet',
                                             maxResults=50,
                                             ).execute()

        for playlist in self.playlists['items']:
            if playlist["id"] == self.playlist_id:
                self.title = playlist["snippet"]["title"]

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']

    @property
    def total_duration(self):
        total = timedelta(hours=0, minutes=0, seconds=0)
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total += duration
        return total

    def show_best_video(self):
        max_like = 0
        url_top = ""
        for likes in self.video_response['items']:
            like = int(likes['statistics']['likeCount'])
            if max_like <= like:
                max_like = like
                url_top = f"https://youtu.be/{likes['id']}"
        return url_top



