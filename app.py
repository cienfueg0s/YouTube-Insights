from googleapiclient.discovery import build
from flask import Flask, request, render_template
from transformers import pipeline

app = Flask(__name__)

# Initialize the summarization pipeline
summarizer = pipeline("summarization")

def get_video_details(video_url):
    api_key = "AIzaSyD3geAPTjcp02ytv1NWEju1566Rpt2lbgA"  # Replace with your actual API key
    try:
        video_id = video_url.split("v=")[-1]
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.videos().list(
            part="snippet,statistics",
            id=video_id
        )
        response = request.execute()
        if response['items']:
            video_details = response['items'][0]
            snippet = video_details['snippet']
            statistics = video_details['statistics']
            description_summary = summarize_text(snippet['description'])
            return {
                "title": snippet['title'],
                "description": snippet['description'],
                "description_summary": description_summary,
                "views": statistics.get('viewCount', 'N/A'),
                "likes": statistics.get('likeCount', 'N/A'),
                "comments": statistics.get('commentCount', 'N/A')
            }
        else:
            return None
    except Exception as e:
        print(f"Error fetching video details: {e}")
        return None

def summarize_text(text):
    summary = summarizer(text, max_length=50, min_length=25, do_sample=False)
    return summary[0]['summary_text']

@app.route("/", methods=["GET", "POST"])
def index():
    video_details = None
    error_message = None
    if request.method == "POST":
        video_url = request.form["video_url"]
        video_details = get_video_details(video_url)
        if video_details is None:
            error_message = "Failed to retrieve video details. Please check the URL and try again."
    return render_template("index.html", video_details=video_details, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)
