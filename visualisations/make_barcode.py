import os
import re
import cv2
import argparse
import numpy as np
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")

def make_barcode(frames_dir, bar_width = 1, save = True):
    '''
    Makes barcode graphic with dir containing png/jpg files.

    Parameters
        frames_dir (string): path to dir with frames (assumes that it ia already sorted)
        bar_width (int) [default = 1]: width of each bar
        save (bool / string) [default = 1]:
            - False: barcode will not be saved
            - True: barcode will be saved with auto-generated file name (barcode_<timestamp>.png)
            - string: barcode will be saved with this string as its filename (does not have to contain file extensions, will be saved as png)

    Returns
        barcode (numpy.ndarray): generated barcode
    '''
    frame_files = sorted(os.listdir(os.path.join(frames_dir)))
    frame_files.sort(key=lambda f: int(re.sub('\D', '', f)))

    barcode_width = bar_width*len(frame_files)

    # use min barcode height
    heights = [cv2.imread(os.path.join(frames_dir, f), cv2.IMREAD_UNCHANGED).shape[0] for f in frame_files]
    barcode_height = min(heights)
    # print("min height = {}".format(barcode_height))

    barcode = np.zeros((barcode_height, barcode_width, 3), np.uint8)
    # print("barcode shape = {}".format(barcode.shape))

    for i, f in zip(range(0, barcode_width, bar_width), frame_files):
        # print(f)
        frame_path = os.path.join(frames_dir, f)
        frame = cv2.imread(frame_path, cv2.IMREAD_UNCHANGED)
        bar = cv2.resize(frame, (bar_width, barcode_height), interpolation = cv2.INTER_AREA)
        barcode[:,i:(i+bar_width)] = bar

    if type(save) is str:
        filename = "{}.png".format(save)
    elif save:
        filename = "barcode_{}.png".format(timestamp)

    # save file
    cv2.imwrite(filename, barcode)

    print("barcode generated: {}".format(filename))
    return barcode


if __name__ == "__main__":
    ap = argparse.ArgumentParser()

    # positional arguments
    ap.add_argument("input", help="path to frames dir")

    # optional arguments
    ap.add_argument("-s", "--save", help="file name to save generated barcode as")
    ap.add_argument("-w", "--width", type=int, help="bar width")
    ap.add_argument("--show", type=bool, help="indicate whether to show generated barcode")

    args = vars(ap.parse_args())
    # print(args)

    frames_dir = args["input"]
    barcode = make_barcode(frames_dir, bar_width=2)
    # print(type(barcode))
    if args["show"]:
        cv2.imshow("Generated Barcode", barcode)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
