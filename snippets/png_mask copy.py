'''
"paste" a png image with transparency over another image
'''
import os
from PIL import Image

from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")

# https://stackoverflow.com/questions/38627870/how-to-paste-a-png-image-with-transparency-to-another-image-in-pil-without-white/38629258

img = Image.open("overlay.png")
background = Image.open("background.png")

# print('img size (w,h): {} \nbg size (w,h): {}'.format(img.size, background.size))

# print(img.mode) # should be RGBA
# print(background.mode) #RGB
background.paste(img, (0, 0), img)

background.save("masked_{}.png".format(timestamp), format="png")

# code to resize if needed
# image = Image.open('og.png')
# new_image = image.resize((1920, 1080))
# new_image.save('og.png')
