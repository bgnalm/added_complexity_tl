import cv2
from PIL import Image, ImageDraw, ImageFont, ImageOps
import string
import random
import numpy as np
import matplotlib.pyplot as plt

possible_font = [
    '/usr/share/fonts/truetype/freefont/FreeMono.ttf',
    '/usr/share/fonts/truetype/fonts-japanese-gothic.ttf',
    '/usr/share/fonts/truetype/padauk/Padauk.ttf',
    '/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-BI.ttf',
]

def combine_images(i1,i2):
    x1, y1 = i1.size
    x2, y2 = i2.size
    x3 = x1 + x2
    y3 = max(y1, y2)
    i3 = Image.new("RGBA",(x3,y3), (255, 255, 255))
    if y1 > y2:
        y2 = (y1 - y2) // 2
    else:
        y2 = y1
    i3.paste(i1, (0, 0))
    i3.paste(i2, (x1,0))
    return i3

def generate_simple_captcha(width, height, num_letters=3, possible_letters=string.ascii_uppercase, possible_fonts=possible_font):
    final_image = Image.new('RGB', (width, height), color='white')

    all_parts = []
    tile_size = width // num_letters
    text = ''
    for i in range(num_letters):
        img = Image.new('RGB', (tile_size, height), color='white')
        d = ImageDraw.Draw(img)
        x_start, x_end = 0, tile_size
        y_start, y_end = 0, height

        font_size = min(random.randint(tile_size//3, tile_size//1), height)
        x = random.randint(x_start, x_end - font_size//1.3)
        y = random.randint(y_start, y_end - font_size//1.3)
        letter = random.choice(possible_letters)
        text += letter
        f = random.choice(possible_fonts)
        font = ImageFont.truetype(f, font_size)
        d.text((x,y), letter, fill=(random.randint(1, 255),random.randint(1, 255), random.randint(1, 255)), font=font)

        min_random = -20
        max_random = 20
        rotation = min_random + ((max_random - min_random) * random.random())
        rotated = img.rotate(rotation, expand=1, fillcolor='white')
        all_parts.append(rotated)

    res = all_parts[0]
    for i in all_parts[1:]:
        res = combine_images(res, i)

    return res, text

def generate_complex_captcha(width, height, num_letters=3, possible_letters=string.ascii_uppercase, possible_fonts=possible_font):
    img, text = generate_simple_captcha(width, height, num_letters, possible_letters)

    draw = ImageDraw.Draw(img)
    for number_of_rectangles in range(random.randint(0, 10)):
        x, y = random.randint(0, width), random.randint(0, height)
        dx, dy = random.randint(-10, 10), random.randint(-10, 10)
        tx, ty = min(max(0, x+dx), width), min(max(0, y+dy), height)
        draw.rectangle(((x,y), (tx, ty)), fill=(random.randint(1, 255),random.randint(1, 255), random.randint(1, 255)))

    for number_of_polygons in range(random.randint(0, 20)):
        # choose a rectangle
        x, y = random.randint(0, width), random.randint(0, height)
        dx, dy = random.randint(-35, 35), random.randint(-35, 35)
        tx, ty = min(max(0, x+dx), width), min(max(0, y+dy), height)
        start_x, end_x = min(x, tx), max(x, tx)
        start_y, end_y = min(y, ty), max(y, ty)

        # choose some points whithin
        points = random.randint(3, 6)
        xs = [random.randint(start_x, end_x) for p in range(points)]
        ys = [random.randint(start_y, end_y) for p in range(points)]
        draw.polygon([(x,y) for x,y in zip(xs, ys)], fill=(random.randint(1, 255),random.randint(1, 255), random.randint(1, 255)))

    return img, text

import time
s = time.time()
img, text = generate_complex_captcha(200, 100, 4)

e = time.time()

print(e-s)
# img.show()

for i in range(3000):
    img, text = generate_simple_captcha(100, 100, 2, possible_fonts=possible_font)
    img.save(f'./images/simple/train/{text}.{i}.png')

for i in range(1000):
    img, text = generate_simple_captcha(100, 100, 2, possible_fonts=possible_font)
    img.save(f'./images/simple/test/{text}.{i}.png')

for i in range(100):
    img, text = generate_complex_captcha(100, 100, 2, possible_fonts=possible_font)
    img.save(f'./images/complex/train/{text}.{i}.png')

for i in range(1000):
    img, text = generate_complex_captcha(100, 100, 2, possible_fonts=possible_font)
    img.save(f'./images/complex/test/{text}.{i}.png')
