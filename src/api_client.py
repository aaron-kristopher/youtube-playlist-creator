import os
from src import utils
from googleapiclient.discovery import build

def get_youtube_service():
    SECRET_API_KEY = os.environ.get("SECRET_API_KEY")
    youtube = build("youtube", "v3", developerKey=SECRET_API_KEY)
    return youtube


def search_videos_from_playlist(playlist_id):
    youtube = get_youtube_service()
    videos = []

    nextPageToken = None

    while True:
        playlist_request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=nextPageToken
        )

        playlist_response = playlist_request.execute()

        video_ids = []
        for item in playlist_response["items"]:
            video_ids.append(item["contentDetails"]["videoId"])

        video_request = youtube.videos().list(
            part = "statistics,snippet",
            id = ",".join(video_ids)
        )

        video_response = video_request.execute()


        for item in video_response["items"]:
            video_title = item["snippet"]["title"]
            episode_number = utils.get_episode_number(video_title)
            video_id = item["id"]
            youtube_link = f"https://youtu.be/{video_id}"

            videos.append(
                        {
                        "title" : video_title,
                        "episode_number" : episode_number,
                        "video_id" : video_id,
                        "url" : youtube_link
                    }
            )

        nextPageToken = playlist_response.get("nextPageToken")

        if not nextPageToken:
            return videos


if __name__ == "__main__":
    playlist_id = "PL5UEpsh7xfCIMBsh7viJcd3HBjEqJt-Do"
    search_videos_from_playlist(playlist_id)
