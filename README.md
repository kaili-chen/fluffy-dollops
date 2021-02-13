# fluffy-dollops
A place for some quick scripts made with python.

# Usage Notes
* Almost all the scripts in this repo can be used with the command line (use `python <script path>.py -h` for quick usage hints)

# Contents
:file_folder: [data_collection](data_collection/)
* :gear: ffmpeg
* :page_facing_up: [get_yt_video.py](data_collection/get_yt_video.py) : gets youtube video as file

:file_folder: [images_videos](images_videos/)
* :page_facing_up: [extract_frames.py](images_videos/extract_frames.py) : gets frames (images) from video file input
* :page_facing_up: [make_barcode.py](images_videos/make_barcode.py) : takes dir (of frames - jpg/png) and generates a barcode
* :page_facing_up: [make_gif.py](images_videos/make_gif.py) : takes dir (of frames - jpg/png) or a video and generates a gif

:file_folder: [snippets](snippets/)
* :information_source: generally discrete code that have not been cleaned for general use

:file_folder: [utility](utility/)
* :file_folder: [boilerplates](utility/boilerplates/)
    * :page_facing_up: [basic_bs_scrapper.py](utility/boilerplates/basic_bs_scrapper.py): beautifulsoup template
    * :page_facing_up: [basic_cmd_line.py](utility/boilerplates/basic_cmd_line.py): cli template
* :card_index: [regex-lib](utility/regex-lib)
    * :information_source: a quick copy for most commonly re-googled regex patterns
    * To use: open `index.html`
* :page_facing_up: [bs_utility.py](utility/bs_utility.py) : beautifulsoup helper functions
* :page_facing_up: [utiltiy.py](utility/utiltiy.py) : general helper functions
