from utility import getBackgroundImage, createPost, getImageText
from constants import *

italian_verb, translation = getImageText(verb = 'conoscere')
background_image = getBackgroundImage()
createPost(background_image, background_color, italian_verb, translation)
