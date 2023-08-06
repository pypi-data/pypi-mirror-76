from PIL import Image
from time import time
""" This module has only one function do() now the easy way is to just give one argument ,which
is the path to the image, but you can give a second argument which is a boolean value. If it is
True then the color value will be in RGB (default is RGB) if it is False it will be HSV """
def do(img_path,rgb=True):
    output = []
    temp = []
    if rgb == True:
        img = Image.open(img_path).convert('RGB')
    else:
        img = Image.open(img_path)
    w,h = img.size
    for i in range(h):
        for j in range(w):
            temp.append(img.getpixel((j,i)))
        output.append(tuple(temp))
        temp.clear()
    return tuple(output)