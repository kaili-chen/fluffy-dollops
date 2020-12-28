'''
"paste" a png image with transparency over another image
'''
import os
from PIL import Image

from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")

# https://stackoverflow.com/questions/38627870/how-to-paste-a-png-image-with-transparency-to-another-image-in-pil-without-white/38629258

img = Image.open("frame500.png")
background = Image.open("ds20_1920_1080.png")

print('img size (w,h): {} \nbg size (w,h): {}'.format(img.size, background.size))

# print(img.mode) # should be RGBA
# print(background.mode) #RGB
background.paste(img, (0, 0), img)

background.save("500_{}.png".format(timestamp), format="png")

# code to resize if needed
# image = Image.open('frame504.png')
# new_image = image.resize((2836, 1080))
# new_image.save('frame5040.png')
