#!/usr/bin/python3
# -*- coding: utf-8 -*-
import colorsys
from PIL import Image, ImageDraw

import hashlib
import os
import math
import numpy as np

class Color:
    def __init__(self,RGB,HLS,HSV):
        self.RGB = RGB
        self.HLS = HLS
        self.HSV = HSV

def genColourList(ColorInput):
    ColorInput.HLS = list(colorsys.rgb_to_hls(ColorInput.RGB[0] / 255, ColorInput.RGB[1] / 255, ColorInput.RGB[2] / 255))

    Base = 360000000
    Split = 2048
    Rotation = Base/Split
    OutputColours = []

    for x in range(1, Split):
        FirstTriadicHue = ((ColorInput.HLS[0] * Base + (Rotation*x)) % Base) / Base
        ColorOutput1 = Color("",[FirstTriadicHue,ColorInput.HLS[1],ColorInput.HLS[2]],"")
        ColorOutput1.RGB = list(map(lambda x: round(x * 255),colorsys.hls_to_rgb(ColorOutput1.HLS[0],ColorOutput1.HLS[1],ColorOutput1.HLS[2])))
        OutputColours.append(ColorOutput1)

    return OutputColours

def to_mnemonic(data: bytes, colourlist):
    if len(data) not in [16, 20, 24, 28, 32]:
        raise ValueError(
            "Data length should be one of the following: [16, 20, 24, 28, 32], but it is not (%d)."
            % len(data)
        )
    h = hashlib.sha256(data).hexdigest()
    b = (
        bin(int.from_bytes(data, byteorder="big"))[2:].zfill(len(data) * 8)
        + bin(int(h, 16))[2:].zfill(256)[: len(data) * 8 // 32]
    )
    result = []
    for i in range(len(b) // 11):
        idx = int(b[i * 11 : (i + 1) * 11], 2)
        result.append(colourlist[idx])
    return result

def drawpolygon(r, n, x, y):
    points = []
    for i in range(0,n):
        points.append(tuple([x+r*math.cos(2*math.pi*i/n), y+r*math.sin(2*math.pi*i/n)]))
    points.append(points[0])
    return points

def drawpalette(colourkey, output_path):
    image = Image.new("RGBA", (500, 500), (255, 255, 255, 0))
    centre = (int(500/2),int(500/2))
    coords = drawpolygon(250-1,len(colourkey),centre[0], centre[1])
    draw = ImageDraw.Draw(image)
    for x in range(0,len(colourkey)):
        draw.polygon((coords[x], coords[x+1], centre), fill=tuple(colourkey[x].RGB))

    img=Image.open("dog.jpg").convert("RGBA")
    img = img.resize((460,460))
    mask_im = Image.new("L", img.size, 0)
    draw2 = ImageDraw.Draw(mask_im)
    draw2.ellipse((0,0,img.size[0],img.size[1]), fill=255)

    back_im = image.copy()

    back_im.paste(img, (int(centre[0]-img.size[0]/2),int(centre[1]-img.size[1]/2)), mask_im)

    finalimage = Image.new("RGBA", (500, 500), (255, 255, 255, 0))
    mask_im2 = Image.new("L", finalimage.size, 0)
    draw3 = ImageDraw.Draw(mask_im2)
    draw3.ellipse((5,5,finalimage.size[0]-5,finalimage.size[1]-5), fill=255)

    finalimage.paste(back_im, (0,0), mask_im2)

    finalimage.save(output_path,'PNG')

#00f782 sessions colour
SessionColour = Color([0x00, 0xf7, 0x82],"","")
colourlist = genColourList(SessionColour)

words = to_mnemonic(os.urandom(32), colourlist)
drawpalette(words, "portrait.png")
