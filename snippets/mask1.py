import os
from PIL import Image

'''
overlay transparent image on background
'''

overlay = Image.open("fg.png")

background = Image.open("bg.png")

print (overlay.mode)    # has to be RGBA
print(background.mode)

background.paste(overlay, (0, 0), overlay)

background.save("overlayed.png", format="png")
