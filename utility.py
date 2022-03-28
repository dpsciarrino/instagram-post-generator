from random import randint
import requests
from bs4 import BeautifulSoup
import sqlite3
from constants import *
from PIL import Image, ImageDraw, ImageFont

def get_page_content(URL):
    req = None
    headers = {
        'Accept-Language': 'en-US,en',
        'Host':'dictionary.cambridge.org',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    }
    try:
        req = requests.get(URL, headers=headers)
    except requests.exceptions.RequestException as e:
        print(e.args)
    
    if req == None:
        print("Response was empty")
        return -1
    
    html = req.text
    bs = BeautifulSoup(html, 'html.parser')

    return bs

def get_translation(verb):
    BASE_URL = 'https://dictionary.cambridge.org/dictionary/italian-english/'
    URL = BASE_URL + verb

    bs = get_page_content(URL)

    senses = [item.text for item in bs.find('div', {'class':'def-body'}).find_all('span', {'class':'trans dtrans', 'lang':'en'})]
    translation = ""
    for sense in senses:
        if senses[0] != sense:
            translation = translation + ", " + sense
        else:
            translation = sense
    
    return translation

def get_random_verb(db_file_name='new.sqlite3', db_table='app_verb') -> str:
    NUM_OF_VERBS = 17619
    _id = randint(1, NUM_OF_VERBS)

    conn = sqlite3.connect(db_file_name)
    cursor = conn.cursor()
    sql = f"""SELECT verb FROM {db_table} WHERE id = {_id}"""
    cursor.execute(sql)
    conn.commit()
    result = cursor.fetchone()
    conn.close()
    try:
        result = result[0]
    except Exception as e:
        print(e.args)
        return None
    
    return result

def get_closest_match(verb):
    '''
    Here, we know that the resulting webpage only gives us 
    suggested search results.

    Choose the first result and search for that.
    '''
    BASE_URL = 'https://dictionary.cambridge.org/spellcheck/italian-english/?q='
    URL = BASE_URL + verb
    bs = get_page_content(URL)

    container = bs.find('div', {'class':'hfl-s lt2b lmt-10 lmb-25 lp-s_r-20'})

    new_verb = ""
    new_verbs_to_try = container.find_all('a')
    for v in new_verbs_to_try:
        new_verb = v.getText()
        translation = get_translation(new_verb)
        if "to" in translation:
            break

    return new_verb, translation


def getImageText(verb = ''):
    '''
    Returns a 2-tuple with the image text to display
    verb, translation
    '''
    if verb == '':
        italian_verb = get_random_verb()
    else:    
        italian_verb = verb
    
    english_translation = ""
    try:
        english_translation = get_translation(italian_verb)
    except AttributeError as e:
        # If the verb does not exist in the cambridge dictionary...
        italian_verb, english_translation = get_closest_match(italian_verb)

    return italian_verb, english_translation


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