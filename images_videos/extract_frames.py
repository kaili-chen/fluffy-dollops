import sys
import os
import argparse
from datetime import datetime

import cv2
# print(cv2.__version__)

def extract_frames(path_in, path_out=None):
    '''
    Gets frame from video file (mp4/avi) as image (1 frame per second).

    Parameters
        path_in (string): path of video (mp4/avi) file
        path_out (string) [default = None]: path of dir to save extracted frames to (if None/invalid dir path, dir automatically created)

    Returns
        path_out (string): path where extracted images are saved to.
    '''
    if path_out is None:
        video_name = path_in[:path_in.rfind(".")].strip()
        video_name = "{} frames".format(video_name)
        if os.path.exists(video_name):
            video_name = "{} frames_{}".format(video_name, datetime.now().strftime("%Y%m%dT%H%M%S"))
        os.mkdir(video_name)
        path_out = video_name

    vidcap = cv2.VideoCapture(path_in)
    count = 0
    success = True
    while success:
        # up video timestamp by 1 second
        vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))
        success,image = vidcap.read()
        # print ('Read frame {}: {}'.format(count, success))

        if not success:
            print("{} frames read.".format(count))
            break

        cv2.imwrite(os.path.join(path_out, "frame%d.png" % count), image)     # save frame as JPEG file
        count = count + 1

    return path_out

if __name__=="__main__":
    ap = argparse.ArgumentParser()

    # positional arguments
    ap.add_argument("input", help="path to video")

    # optional arguments
    ap.add_argument("-d", "--dest", help="path to save frame images [default = current dir]")
    args = vars(ap.parse_args())
    # print(args)
    path_in = args["input"]
    if os.path.exists(path_in) and os.path.isfile(path_in):
        file_ext = path_in[path_in.rfind(".")+1:]
        if file_ext not in ["mp4", "avi", "webm", "mkv"]:
            print("error: input ({}) not mp4/avi/webm, exiting...".format(path_in))
            sys.exit()
    else:
        print("error: input ({}) either does not exist or not a file, exiting...")
        sys.exit()

    path_out = args["dest"]
    if path_out != None:
        if not os.path.exists(path_out) or not os.path.isdir(path_out):
            path_out = None
            print("note: output path does not exist or is not a valid dir, will proceed with created dir.")

    extract_frames(path_in, path_out)
