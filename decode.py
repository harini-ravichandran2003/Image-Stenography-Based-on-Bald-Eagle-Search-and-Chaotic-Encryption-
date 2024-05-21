import cv2
import imageio
import xlsxwriter
from PIL import Image
import openpyxl 
import binascii
import tkinter as tk
from tkinter import filedialog
def LSBDecode(stegoimage):
    input_image = Image.open(stegoimage)
    width, height = input_image.size 
    bitdepth = 24
    if len(input_image.getpixel((0, 0)))==4:
        bitdepth = 32

    i = 0
    j = 0
    s=''
    for k in range(0,30,6):
        if bitdepth==24:
            r, g, b = input_image.getpixel((i, j))
        else:
            r, g, b, a = input_image.getpixel((i, j))

        r1 = format(r,'08b')
        g1 = format(g,'08b')
        b1 = format(b,'08b')
        s = s+r1[6]+r1[7]+g1[6]+g1[7]+b1[6]+b1[7]      
        j = j+1
        if j==width:
            i = i+1
            j = 0
    swidth = int(s[:15],2) 
    sheight = int(s[15:],2)  
    output_image = Image.new(mode="RGB", size=(swidth, sheight))
    s = ''
    e = 0
    f = 0
    while i<width:
        while j<height:
            if e==swidth:
                break            
            if bitdepth==24:
                r, g, b = input_image.getpixel((i, j))
            else:
                r, g, b, a = input_image.getpixel((i, j))
            r1 = format(r,'08b')
            g1 = format(g,'08b')
            b1 = format(b,'08b')
            s = s+r1[6]+r1[7]
            if len(s)==24:
                rs = int(s[0:8],2)
                gs = int(s[8:16],2)
                bs = int(s[16:24],2)
                output_image.putpixel((e,f),(rs,gs,bs))
                f = f + 1
                if f==sheight:
                    f = 0
                    e = e + 1
                s=''
            s = s+g1[6]+g1[7]
            if len(s)==24:
                rs = int(s[0:8],2)
                gs = int(s[8:16],2)
                bs = int(s[16:24],2)
                output_image.putpixel((e,f),(rs,gs,bs))
                f = f + 1
                if f==sheight:
                    f = 0
                    e = e + 1
                s=''
            s = s+b1[6]+b1[7]
            if len(s)==24:
                rs = int(s[0:8],2)
                gs = int(s[8:16],2)
                bs = int(s[16:24],2)
                output_image.putpixel((e,f),(rs,gs,bs))
                f = f + 1
                if f==sheight:
                    f = 0
                    e = e + 1
                s=''
            j = j + 1
        j = 0
        i = i + 1
    output_image.save('decoded_image.png')
    print("\nDecoded Successfully...")
    print("\nSaved As decoded_image.png...")

LSBDecode('steg_img.png')