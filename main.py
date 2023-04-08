from tkinter import *
import tkinter as tk

from PIL import Image

def genData(data):
    newd = []
    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd

def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)
    for i in range(lendata):
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]
        for j in range(0, 8):
            if datalist[i][j] == '0' and pix[j] % 2 != 0:
                pix[j] -= 1
            elif datalist[i][j] == '1' and pix[j] % 2 == 0:
                if pix[j] != 0:
                    pix[j] -= 1
                else:
                    pix[j] += 1
        if i != lendata - 1:
            if pix[-1] % 2 != 0:
                pix[-1] -= 1
        else:
            if pix[-1] % 2 == 0:
                if pix[-1] != 0:
                    pix[-1] -= 1
                else:
                    pix[-1] += 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


def encryption(img, data):
    size = img.size[0]
    (x, y) = (0, 0)
    for pixel in modPix(img.getdata(), data):
        img.putpixel((x, y), pixel)
        if size-1 == x:
            x = 0
            y += 1
        else:
            x += 1


def encode(img, data, new_img_name):
    image = Image.open(img, 'r')
    if len(data) == 0:
        raise ValueError('Data is empty')

    newimg = image.copy()
    encryption(newimg, data)

    new_img_name += '.png'
    newimg.save(new_img_name, str(new_img_name.split(".")[1].lower()))

def decode(img, strvar):
    image = Image.open(img, 'r')
    data = ''
    imgdata = iter(image.getdata())
    while True:
        pixels = [value for value in imgdata.__next__()[:3] +
                  imgdata.__next__()[:3] +
                  imgdata.__next__()[:3]]

        binstr = ''

        for i in pixels[:8]:
            if i % 2 == 0:
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))

        if pixels[-1] % 2 != 0:
            strvar.set(data)
            return data

def encode_image():
    encode_wn = Toplevel(root)
    encode_wn.title("Encode an Image")
    encode_wn.geometry('600x220')
    encode_wn.resizable(0, 0)
    encode_wn.config(bg='pink')
    Label(encode_wn, text='Encode an Image', font=("Comic Sans MS", 15), bg='AntiqueWhite').place(x=220, rely=0)

    Label(encode_wn, text='Enter the path to the image(with extension):', font=("Times New Roman", 13),
          bg='AntiqueWhite').place(x=10, y=50)
    Label(encode_wn, text='Enter the data to be encoded:', font=("Times New Roman", 13), bg='AntiqueWhite').place(
        x=10, y=90)
    Label(encode_wn, text='Enter the output file name (without extension):', font=("Times New Roman", 13),
          bg='AntiqueWhite').place(x=10, y=130)

    img_path = Entry(encode_wn, width=35)
    img_path.place(x=350, y=50)

    text_to_be_encoded = Entry(encode_wn, width=35)
    text_to_be_encoded.place(x=350, y=90)

    after_save_path = Entry(encode_wn, width=35)
    after_save_path.place(x=350, y=130)

    Button(encode_wn, text='Encode the Image', font=('Helvetica', 12), bg='PaleTurquoise', command=lambda:
        encode(img_path.get(), text_to_be_encoded.get(), after_save_path.get())).place(x=220, y=175)

def decode_image():
    decode_wn = Toplevel(root)
    decode_wn.title("Decode an Image")
    decode_wn.geometry('600x300')
    decode_wn.resizable(0, 0)
    decode_wn.config(bg='pink')

    Label(decode_wn, text='Decode an Image', font=("Comic Sans MS", 15), bg='Bisque').place(x=220, rely=0)

    Label(decode_wn, text='Enter the path to the image (with extension):', font=("Times New Roman", 12),
          bg='Bisque').place(x=10, y=50)

    img_entry = Entry(decode_wn, width=35)
    img_entry.place(x=350, y=50)

    text_strvar = StringVar()

    Button(decode_wn, text='Decode the Image', font=('Helvetica', 12), bg='PaleTurquoise', command=lambda:
       decode(img_entry.get(), text_strvar)).place(x=220, y=90)

    Label(decode_wn, text='Text that has been encoded in the image:', font=("Times New Roman", 12), bg='Bisque').place(
        x=180, y=130)

    text_entry = Entry(decode_wn, width=94, text=text_strvar, state= 'disabled')
    text_entry.place(x=15, y=160, height=100)


root = tk.Tk()
root.title('Project Image Steganography')
root.geometry('300x200')
root.resizable(0, 0)
root.config(bg='purple')

Label(root, text='Project Image Steganography', font=('Comic Sans MS', 15), bg='purple',
      wraplength=300).place(x=40, y=0)

Button(root, text='Encode', width=25, font=('Times New Roman', 13), bg='SteelBlue', command=encode_image).place(
    x=30, y=80)

Button(root, text='Decode', width=25, font=('Times New Roman', 13), bg='SteelBlue', command=decode_image).place(
    x=30, y=130)

root.update()
root.mainloop()
