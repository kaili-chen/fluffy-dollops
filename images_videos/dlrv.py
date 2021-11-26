"""
script to download video from a reddit post using url
"""

import urllib.request
import json
import subprocess
import os
import argparse

def merge_video_audio(video_path, audio_path, output_filename):
    '''uses ffmpeg (needs to be installed on device) to combine video and audio file
    Parameters:
        video_path::str
            video mp4 file path
        audio_path::str
            audio mp4 file path
        output_filename::bool
            video output path

    Returns:
        None
    '''
    # ffmpeg -i <video> -i <audio> -c:v copy -c:a aac output.mp4
    subprocess.call('ffmpeg -i {} -i {} -c:v copy -c:a aac {}'.format(video_path, audio_path, output_filename), shell=True)

    # cleanup temp files
    if os.path.isfile(video_path): os.remove(video_path)
    if os.path.isfile(audio_path): os.remove(audio_path)

def main(url, output_path='output.mp4', use_file=False):
    '''gets reddit url / read json file to download video
    Parameters:
        url::str
            reddit post url / json file path
        output_path::str
            output mp4 path, default = 'output.mp4'
        use_file::bool
            if true, reads url as json file path instead of reddit url, default = False

    Returns:
        None
    '''
    if use_file:
        print('reading file')
        res = json.load(open(url, 'r'))
    else:
        print('reading url')
        url = url[:-1]+'.json'
        res_obj = urllib.request.urlopen(url)
        res = json.load(res_obj)

    post_item = res[0]
    post_data = post_item['data']
    video_info = post_data['children'][0]['data']['secure_media']
    video_url = video_info['reddit_video']['fallback_url']
    audio_url = video_url[:video_url.find('DASH_')+len('DASH_')]+'audio.mp4?source=fallback'

    print('downloading video...')
    urllib.request.urlretrieve(video_url, filename='output_video.mp4')
    print('downloading audio...')
    urllib.request.urlretrieve(audio_url, filename='output_audio.mp4')

    merge_video_audio('output_video.mp4', 'output_audio.mp4', output_path)

if __name__ == '__main__':
    
    # initialise parser
    parser = argparse.ArgumentParser(description=__doc__)
    # add positional arguments
    parser.add_argument("url")
    # add optional arguments
    parser.add_argument('-o', '--output', required=False, help="file path to save resulting mp4 file", type=str)
    parser.add_argument('-f', '--usefile', required=False, help="if true, reads url as json file path", type=bool)

    # read arguments
    args = parser.parse_args()

    # run main method
    main(args.url, output_path=args.output)
