import os
import csv
from dotenv import load_dotenv
from googleapiclient.discovery import build
from datetime import datetime, timezone

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")
if not API_KEY:
    raise ValueError("YOUTUBE_API_KEY was not found.")
DATE_TODAY = datetime.now().strftime("%d-%m-%y")

class YoutubeData:
    """Model that gets youtube's channel data and saves them as .csv file."""

    def __init__(self, youtube_channel, start_date=None):
        """Initialize model's core attributes."""
        self.youtube_channel = youtube_channel
        self.channel_name = youtube_channel.removeprefix('@').lower()

        if start_date is None:
            start_date = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.start_date = start_date

        self.youtube = build(
            'youtube',
            'v3',
            developerKey=API_KEY,
        )

    def get_uploads_playlist_id(self):
        """Get video's playlist IDs."""
        request = self.youtube.channels().list(
            part="snippet,statistics,contentDetails",
            forHandle=self.youtube_channel,
        )       
        response = request.execute()
        channel = response['items'][0]
        uploads_playlist_id = channel['contentDetails']['relatedPlaylists']['uploads']
        return uploads_playlist_id

    def get_video_ids(self):
        """Get single videos IDs."""
        video_ids = []
        next_page_token = None
        playlist_id = self.get_uploads_playlist_id()

        while True:
            request = self.youtube.playlistItems().list(
                part="contentDetails",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token,
            )

            response = request.execute()

            for item in response['items']:
                published_at = item['contentDetails']['videoPublishedAt']
                published_date = datetime.fromisoformat(published_at.replace('Z','+00:00'))
                if published_date >= self.start_date:
                    video_ids.append(item['contentDetails']['videoId'])

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                        break
        return video_ids

    def get_videos_resources(self):
        """Get videos data."""
        video_ids = self.get_video_ids()
        videos = []

        for start in range(0, len(video_ids), 50):
            batch = video_ids[start : start + 50]

            request = self.youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=','.join(batch),
            )

            response = request.execute()

            for video in response['items']:
                snippet = video['snippet']
                statistics = video['statistics']
                content_details = video['contentDetails']
                videos.append(
                    {
                        'video_id': video['id'],
                        'title': snippet['title'],
                        'published_at': snippet['publishedAt'],
                        'views': int(statistics.get('viewCount', 0)),
                        'likes': int(statistics.get('likeCount', 0)),
                        'comments': int(statistics.get('commentCount', 0)),
                        'duration': content_details['duration'],
                    }
                )
        return videos

    def download_csv(self):
        """Saves the videos resources in a .csv file."""
        videos = self.get_videos_resources()

        with open(f"data/{self.channel_name}({DATE_TODAY}).csv", "w", newline="", encoding="utf-8") as file:
            fieldnames = [
                'video_id',
                'title',
                'published_at',
                'views',
                'likes',
                'comments',
                'duration',
            ]
            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames,
            )
            writer.writeheader()
            writer.writerows(videos)

        filename = f"data/{self.channel_name}({DATE_TODAY}).csv"
        return filename

#===============================================================================================================
if __name__ == "__main__":
    data = YoutubeData("@PPPiter_Official").download_csv()
    print(f"The file has been saved in \n\t{data}")
