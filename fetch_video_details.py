from googleapiclient.discovery import build
from flask import Flask, request, render_template

app = Flask(__name__)

def get_video_details(video_url, api_key):
    # Extract the video ID from the URL
    video_id = video_url.split("v=")[-1]

    # Set up the YouTube API client
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Fetch video details including statistics
    request = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    )
    response = request.execute()

    if response['items']:
        video_details = response['items'][0]
        snippet = video_details['snippet']
        statistics = video_details['statistics']
        return {
            "title": snippet['title'],
            "description": snippet['description'],
            "views": statistics.get('viewCount', 'N/A'),
            "likes": statistics.get('likeCount', 'N/A'),
            "comments": statistics.get('commentCount', 'N/A')
        }
    else:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    video_details = None
    if request.method == "POST":
        video_url = request.form["video_url"]
        api_key = "YOUR_API_KEY"  # Replace with your actual API key
        video_details = get_video_details(video_url, api_key)
    return render_template("index.html", video_details=video_details)

if __name__ == "__main__":
    app.run(debug=True)
