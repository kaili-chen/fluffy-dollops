import argparse
import os
import sys
import csv
import subprocess
from pytube import YouTube

# https://pypi.org/project/pytube3/

# UTILITY FUNCTIONS
def is_yt_url(url):
    '''
    Checks if url provided is a youtube url

    Parameters:
        url (string):  url

    Returns:
        (boolean) indicating if url provided is a youtube url
    '''
    if url.find('youtube.com/watch?v=') > -1 or url.find('youtu.be/') > -1:
        return True
    return False


def read_file(path, skip=None):
    '''
    Returns lines from files.

    Parameters:
        path (string):  path of file
        skip (function) [default = None]: function that returns a boolean to check if whether to skip a line (True -> Do not skip, False -> Skip)
    Returns:
        lines (list): list of lines from file
    '''

    def read_txt(path):
        file = open(path, "r")
        if skip:
            lines = [line.strip() for line in file.readlines() if skip(line)]
        else:
            lines = [line.strip() for line in file.readlines()]
        return lines

    methods = {
        'txt': read_txt(path)
    }

    is_file = os.path.isfile(path)
    if is_file:
        file_ext = input[input.rfind('.')+1:]
        if file_ext in methods.keys():
            lines = methods[file_ext]
            # print("file ext = {}".format(file_ext))
            return lines
        else:
            return None
    return None


# FUNCTIONS
def download_video(url, max_tries = 20, video_only = False):
    '''
    Downloads video from youtube url

    Parameters:
        url (string): youtube url
        max_tries (int) [default = 20]: number of times to try downloading link before aborting
        video_only (bool) [default = False]:
            if True: might get video with no audio but higher resolution
            if False / None: always get mp4 (if any)
    Returns:
        if successful: file path of downloaded video
        if unsuccessful: None
    '''

    # TODO: add path_out
    # TODO: deal with seperate audio and video files

    # https://pytube3.readthedocs.io/en/latest/user/quickstart.html#working-with-streams

    passed = False
    try_count = 0
    while not passed and try_count < max_tries:
        # odd error occurs at times, refer to https://github.com/nficano/pytube/issues/393 -hence the while loop
        try:
            yt = YouTube(url)
            output_filename = "output.mkv"

            print("downloading...")
            if video_only:
                dl = yt.streams.filter(only_video=True).order_by('resolution')[-1].download()
            else:
                # dl = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download()
                vid_stream = yt.streams.filter(only_video=True).order_by('resolution')[-1]
                # print(vid_stream)
                # print()
                if not vid_stream.includes_video_track:
                    dl = vid_stream.download()
                    return dl

                vid = vid_stream.download("temp", filename="temp_vid")
                # print(vid)

                audio_stream = yt.streams.filter(only_audio=True).order_by('abr')[-1]
                audio = audio_stream.download("temp", filename="temp_audio")
                # print(audio_stream.includes_audio_track)
                # print(audio)

                # join video and audio with ffmpeg
                cmd = './ffmpeg -y -i temp/temp_audio.webm  -r 30 -i temp/temp_vid.webm  -filter:a aresample=async=1 -c:a flac -c:v copy {}'.format(output_filename)
                subprocess.call(cmd, shell=True, stderr=subprocess.DEVNULL) #suppress output
                os.rename(os.path.join(os.getcwd(), output_filename), os.path.join(os.getcwd(), "{}.mkv".format(yt.title)))

                # subprocess.call(cmd, shell=True)
                    # change webm to mp4
                    # cmd = 'ffmpeg -i input.mp4 output.webm'
                # except subprocess.CalledProcessError:
                #     print("subproc error")

                # clean up temp files and folder
                os.remove(vid)
                os.remove(audio)
                os.rmdir("./temp")

                dl = os.path.join(os.getcwd(), "{}.mkv".format(yt.title))
                # dl = os.path.join(os.getcwd(), output_filename)
                # dl = yt.streams.filter(only_video=True).order_by('resolution')[-1].download()

            print(dl)

            passed = True
            try_count = 0
            return dl

        except Exception as e:
            print(str(e))
            try_count += 1
            print('failed, count={}'.format(try_count))

    print('failed: {}'.format(url))

    return None

if __name__ == "__main__":
    ap = argparse.ArgumentParser()

    # positional arguments
    ap.add_argument('input', help='input file or youtube url')

    # optional arguments
    ap.add_argument('-v', '--video', type=bool, help='indicate whether to download video only')

    args = vars(ap.parse_args())
    # print(args)
    # checks if input is a file path
    input = args['input']
    is_file = os.path.isfile(input)
    if is_file:
        print("File found")
        lines = read_file(input, skip=is_yt_url)
        for line in lines:
            download_video(line, video_only=args['video'])
    elif is_yt_url(input):
        print("URL found: {}".format(input))
        download_video(input, video_only=args['video'])
    else:
        print("no file/url found")
