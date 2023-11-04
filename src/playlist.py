import datetime
from googleapiclient.discovery import build
import os
import isodate

API_KEY: str = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=API_KEY)


class PlayList():
    def __init__(self, playlist_id) -> None:
        self.playlist_id = playlist_id
        self.playlist = self.get_playlist_info()
        self.title = self.playlist['items'][0]['snippet']['localized']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        self.playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        self.video_ids = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(self.video_ids)
                                                    ).execute()

    def get_playlist_info(self) -> dict:
        """Получаем данные по плэйлистам канала"""
        playlists = youtube.playlists().list(id=self.playlist_id, part='snippet',
                                             maxResults=50).execute()
        return playlists

    @property
    def total_duration(self):
        """Суммарня длительность плейлиста"""
        result = datetime.timedelta()

        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            result += duration
        return result

    def show_best_video(self):
        global best_video
        likes = 0

        for video_id in self.video_ids:

            video_request = youtube.videos().list(
                part='statistics',
                id=video_id
            ).execute()

            likes_count = video_request['items'][0]['statistics']['likeCount']

            if int(likes_count) > likes:
                likes = int(likes_count)
                best_video = f"https://youtu.be/{video_request['items'][0]['id']}"

        return best_video
