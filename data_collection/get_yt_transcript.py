from youtube_transcript_api import YouTubeTranscriptApi, _errors
import re
import json
import argparse

# https://pypi.org/project/youtube-transcript-api/

def get_video_id(url):
    '''
    Returns the youtube video id from a youtube url.

    Parameter:
    - url (string): youtube url

    Returns:
    - video_id (string): video id of youtube video if found
    '''
    v_index = url.rfind('v=') # get the index of 'v=' in (youtube) url
    video_id = url[v_index+2:]
    return video_id

def get_transcript(url):
    video_id = get_video_id(url)
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(['en', 'en-US', 'en-UK'])
        transcript_text = transcript.fetch()
    except _errors.TranscriptsDisabled:
        print("subtitles are disabled for the video at this url: {}".format(url))
        return None

    only_text = [e['text'] for e in transcript_text]
    only_text = '\n'.join(only_text)    # each subtitle in a separate time
    return only_text

if __name__ == '__main__':
    # TODO: add youtube url check
    ap = argparse.ArgumentParser()

    # positional arguments
    ap.add_argument('url', help='youtube url')
    ap.add_argument('filename', help='filename of transcript txt')

    args = vars(ap.parse_args())

    filepath = '{}.txt'.format(args['filename'])
    transcript = get_transcript(args['url'])
    if transcript:
        with open(filepath) as output:
            output.write(transcript)

        print('{} saved'.format(filepath))
