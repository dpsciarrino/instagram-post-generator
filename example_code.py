from PIL import Image, ImageDraw, ImageFont

# Add the features of the image
text1 = 'assaggiare'
text2 = '(to taste/sample)'

img_name = 'feature-image-with-python.png'

color = 'yellow_green' # grey,light_blue,blue,orange,purple,yellow,green

font = './Roboto-Bold.ttf'

# Find the background image
background = Image.open('02.png')
#foreground = Image.open('python-logo.png')

# Create the color templates
colors = {
    'dark_blue':{'c':(27,53,81),'p_font':'rgb(255,255,255)','s_font':'rgb(255, 212, 55)'},
    'grey':{'c':(70,86,95),'p_font':'rgb(255,255,255)','s_font':'rgb(93,188,210)'},
    'light_blue':{'c':(93,188,210),'p_font':'rgb(27,53,81)','s_font':'rgb(255,255,255)'},
    'blue':{'c':(23,114,237),'p_font':'rgb(255,255,255)','s_font':'rgb(255, 255, 255)'},
    'orange':{'c':(242,174,100),'p_font':'rgb(0,0,0)','s_font':'rgb(0,0,0)'},
    'purple':{'c':(114,88,136),'p_font':'rgb(255,255,255)','s_font':'rgb(255, 212, 55)'},
    'red':{'c':(255,0,0),'p_font':'rgb(0,0,0)','s_font':'rgb(0,0,0)'},
    'yellow':{'c':(255,255,0),'p_font':'rgb(0,0,0)','s_font':'rgb(27,53,81)'},
    'yellow_green':{'c':(232,240,165),'p_font':'rgb(0,0,0)','s_font':'rgb(0,0,0)'},
    'green':{'c':(65, 162, 77),'p_font':'rgb(217, 210, 192)','s_font':'rgb(0, 0, 0)'}
}

# Add color to the package
def add_color(bg_image, c, transparency):
    color = Image.new('RGB', bg_image.size, c)
    mask = Image.new('RGBA', bg_image.size, (0,0,0,transparency))
    return Image.composite(bg_image, color, mask).convert('RGB')

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

def add_text(img, color, text1, text2, logo=False, font='Roboto-Bold.ttf', font_size=75):
    p_font = color['p_font']
    s_font = color['s_font']

    # Starting position of the message
    font1 = ImageFont.truetype(font, size=80)
    font2 = ImageFont.truetype(font, size=40)

    if logo == False:
        center_text(img, font1, text1, text2, p_font, s_font, font2 = font2)
    else:
        draw = ImageDraw.Draw(img)
        img_w, img_h = img.size
        height = img_h // 3
        text1_offset = (img_w // 4, height)
        text2_offset = (img_w // 4, height + img_h // 5)
        draw.text(text1_offset, text1, fill=p_font, font=font1)
        draw.text(text2_offset, text2, fill=s_font, font=font2)
    return img

def add_logo(background, foreground):
    bg_w, bg_h = background.size
    img_w, img_h = foreground.size
    img_offset = (20, (bg_h - img_h) // 2)
    background.paste(foreground, img_offset, foreground)
    return background

def write_image(background, color, text1, text2, foreground=''):
    background = add_color(background, color['c'], 95)
    if not foreground:
        add_text(background, color, text1, text2)
    else:
        add_text(background, color, text1, text2, logo=True)
        add_logo(background, foreground)
    return background


if __name__ == '__main__':
    background = write_image(background, colors[color], text1, text2)
    background.save(img_name)