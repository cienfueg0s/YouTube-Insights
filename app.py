from googleapiclient.discovery import build
from flask import Flask, request, render_template
from transformers import pipeline

app = Flask(__name__)

# Initialize the summarization pipeline
summarizer = pipeline("summarization")


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

    print(response)  # Print the API response for debugging

    if response['items']:
        video_details = response['items'][0]
        snippet = video_details['snippet']
        statistics = video_details['statistics']

        # Summarize the description
        description_summary = summarize_text(snippet['description'])

        return {
            "title": snippet['title'],
            "description": snippet['description'],
            "description_summary": description_summary,  # Add summary to return
            "views": statistics.get('viewCount', 'N/A'),
            "likes": statistics.get('likeCount', 'N/A'),
            "comments": statistics.get('commentCount', 'N/A')
        }
    else:
        return None


def summarize_text(text):
    # Generate summary using the summarization pipeline
    summary = summarizer(text, max_length=50, min_length=25, do_sample=False)
    return summary[0]['summary_text']


@app.route("/", methods=["GET", "POST"])
def index():
    video_details = None
    if request.method == "POST":
        video_url = request.form["video_url"]
        api_key = "AIzaSyD1-XgJ4RdpltTo01vaLFEWhrCUk989vYo"  # Your new API key
        video_details = get_video_details(video_url, api_key)
    return render_template("index.html", video_details=video_details)


if __name__ == "__main__":
    app.run(debug=True)
