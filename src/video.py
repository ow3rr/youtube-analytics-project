from googleapiclient.discovery import build
import os

API_KEY: str = os.getenv('YOUTUBE_API_KEY')


class Video:
    def __init__(self, video_id: str) -> None:
        try:
            self.video_id = video_id
            self.video = self.get_video_data()
            self.title = self.video['items'][0]['snippet']['title']
            self.url = f"https://www.youtube.com/channel/{self.video_id}"
            self.view_count = int(self.video['items'][0]['statistics']['viewCount'])
            self.like_count = int(self.video['items'][0]['statistics']['likeCount'])
        except IndexError:
            self.video_id = video_id
            self.video = None
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None
            print('Ты не пройдешь!!!')

    def __str__(self):
        return self.title

    def get_video_data(self) -> dict:
        youtube = self.get_service()
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.video_id).execute()
        return video_response

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=API_KEY)


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
