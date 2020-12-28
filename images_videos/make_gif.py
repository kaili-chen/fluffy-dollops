import glob
from PIL import Image
import argparse
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")

def make_gif(file_in, file_out):
    '''
    Produces a gif with png files in dir (file_in).

    Parameters:
    - file_in (string): path to dir with png files to be used as frames for gif [default: ./]
    - file_out (string): file path to save gif as [default: ./output_<datetime>.gif]

    Returns:
    - file_out (string): file path of gif made
    '''
    file_in = "{}/*.png".format(file_in)

    if not file_out:
        file_out = "./output{}.gif".format(timestamp)

    img, *imgs = [Image.open(f) for f in sorted(glob.glob(file_in))]
    # duration is in milliseconds
    img.save(fp=file_out, format="GIF", append_images=imgs, save_all=True, duration=200)

    return file_out

if __name__ == "__main__":
    ap = argparse.ArgumentParser()

    # positional arguments
    ap.add_argument('input', help='path to dir with png files to be used as frames for gif [default: ./]')

    # optional arguments
    ap.add_argument('-d', '--dest', help='file path to save gif as [default: ./output_<datetime>.gif]')

    args = vars(ap.parse_args())

    print(make_gif(args['input'], args['dest']))
