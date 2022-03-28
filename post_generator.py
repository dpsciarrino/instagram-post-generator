from utility import getBackgroundImage, createPost
from constants import *

text1, text2 = "Text Line 1", "Text Line 2"
background_image = getBackgroundImage()
createPost(background_image, background_color, text1, text2)
