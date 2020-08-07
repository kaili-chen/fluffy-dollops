from youtube_transcript_api import YouTubeTranscriptApi
import re

# def get_video_id()

# def get_transcript()

yt_url = "https://www.youtube.com/watch?v=CmS5rlX9cDA"

v_index = yt_url.rfind('v=')    # get the index of 'v=' in yt_url
video_id = yt_url[v_index+2:]

transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

transcript = transcript_list.find_transcript(['en-US'])

print(transcript)
