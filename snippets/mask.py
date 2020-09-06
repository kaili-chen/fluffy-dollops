import cv2
import numpy as np
from datetime import datetime

'''
was an attempt to overlay transparent image on background - does not do that but created some interesting visuals
'''

timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")

# background and overlay has to be same size, assumed to be here
background = cv2.imread('bg.png')
overlay = cv2.imread('fg.png')

image_new = np.maximum(overlay, background)

image_new = cv2.bitwise_and(overlay, background)
cv2.imwrite('combined_{}.png'.format(timestamp), image_new)
