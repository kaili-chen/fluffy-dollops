import glob
from PIL import Image
import argparse
from datetime import datetime
import os
import re

import extract_frames

timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")

def make_gif(file_in, file_out, frame_duration=100):
    '''
    Produces a gif with png files in dir (file_in).

    Parameters:
    - file_in (string): path to dir with png files to be used as frames for gif [default: ./]
    - file_out (string): file path to save gif as [default: ./output_<datetime>.gif]
    - frame_duration=100 (int): duration between each frame [default = milliseconds]

    Returns:
    - file_out (string): file path of gif made
    '''
    # TODO: also handle jpg & jpeg files
    # only loads in png files
    file_in = "{}/*.png".format(file_in)

    if not file_out:
        file_out = "./output{}.gif".format(timestamp)

    frames = sorted(glob.glob(file_in))
    # sort frames by number e.g. frame 10 before frame 2
    frames.sort(key=lambda f: int(re.sub('\D', '', f)))

    frames = [Image.open(f) for f in frames]
    # duration is in milliseconds (500 milliseconds = 1/2 second)
    frames[0].save(fp=file_out, format="GIF", append_images=frames[1:], save_all=True, duration=frame_duration)

    return file_out

if __name__ == "__main__":
    ap = argparse.ArgumentParser()

    # TODO check if input is even valid

    # positional arguments
    ap.add_argument('input', help='path to dir with png files to be used as frames for gif [default: ./]')

    # optional arguments
    ap.add_argument('-d', '--dest', help='file path to save gif as [default: ./output_<datetime>.gif]')
    ap.add_argument('-t', '--duration', type=int, default=100, help='duration between each frame [default = 100 milliseconds]')

    args = vars(ap.parse_args())
    input_item = args['input']
    if not os.path.isdir(input_item): 
        print('input is not dir')
        # change input dir to extracted frames from video
        input_item = extract_frames.extract_frames(input_item)
        # TODO: delete this frames dir after
    print(make_gif(input_item, args['dest'], frame_duration=args['duration']))
