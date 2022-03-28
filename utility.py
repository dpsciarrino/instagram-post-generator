# CODE ADAPTED FROM JC Chouinard FROM ARTICLE:
# https://www.jcchouinard.com/create-feature-image-with-python-pillow/

from random import randint
from constants import *
from PIL import Image, ImageDraw, ImageFont

def get_image_files() -> list:
    '''
    Retrieve all image files from the 'img' directory.

    Returns a list.
    '''
    img_files = []
    for img in IMG_PATH.iterdir():
        img_files.append(img)
    return img_files


def getBackgroundImage():
    img_files = get_image_files()
    background_image = img_files[randint(0, len(img_files)-1)]
    return Image.open(background_image)


# Make sure the text is centered
def center_text(img, font, text1, text2, fill1, fill2, font2=''):
    if font2 == '':
        font2 = font

    # Initialize drawing on the image
    draw = ImageDraw.Draw(img)

    # Get width and height of the image
    w, h = img.size

    # Get text1 size
    t1_width, t1_height = draw.textsize(text1, font)
    # Get text2 size
    t2_width, t2_height = draw.textsize(text2, font2)

    # Horizontal center align text1
    p1 = ( (w-t1_width)/2, h // 3 )

    # Horizontal center align text2
    p2 = ((w-t2_width)/2, h//3 + h//5)

    # Draw text on top of image
    draw.text(p1, text1, fill=fill1, font=font)
    # Draw text on top of image
    draw.text(p2, text2, fill=fill2, font=font2)
    return img


def add_text(img, color, text1, text2, font='Roboto-Bold.ttf', font_size1=80, font_size2=40):
    p_font = color['p_font']
    s_font = color['s_font']

    # Starting position of the message
    font1 = ImageFont.truetype(font, size=font_size1)
    font2 = ImageFont.truetype(font, size=font_size2)

    center_text(img, font1, text1, text2, p_font, s_font, font2 = font2)

    return img


def add_color(bg_image, c, transparency):
    color = Image.new('RGB', bg_image.size, c)
    mask = Image.new('RGBA', bg_image.size, (0,0,0,transparency))
    return Image.composite(bg_image, color, mask).convert('RGB')


def write_image(background, color, text1, text2, transparency = 95):
    background = add_color(background, color['c'], transparency)
    add_text(background, color, text1, text2)
    return background


def createPost(background_image, background_color, top_text, bottom_text):
    post_img_name = top_text + ".png"
    post_img_path = POST_PATH / post_img_name

    background = write_image(background_image, colors[background_color], top_text, bottom_text)
    background.save(post_img_path)
    print("New Post: ", post_img_path)