import os
import sys
import tkinter 
import cv2
from PIL import Image, ImageTk
import numpy as np
from functools import partial
import time

num = 0
IM = []

images_rgb = []
images_rect = []
images_tk = []
newImages = list()

filePathP = []

height_list = []
width_list = []
rect_left_list = []
imagetk_list = list()

def toFinish():
    finishPath = 'E:/DATA/ImageTagChangeForSD/ImageTagChangeForSD'
    sys.path.append(finishPath)
    import finishTest
    finishTest

def makeImageTKList(path,RT):
    global images_tk
    global dir_pathP
    global filesP
    dir_pathP = path.replace('\\','/')
    
    filesP = os.listdir(dir_pathP)
    print(filesP)
    for e,file in enumerate(filesP):
        filePathP.append(dir_pathP + '/' + file)

        image_bgr = cv2.imread(filePathP[e])
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB) # imreadはBGRなのでRGBに変換
        h, w, _ = image_rgb.shape
        images_rgb.append(image_rgb)

        height_list.append(h)
        width_list.append(w)
        rect_left_list.append(int(round(w / 2)) - 256)
        image_rect = cv2.rectangle(image_rgb,(rect_left_list[e],0),(rect_left_list[e] + 512,512),(255,255,255),10)

        images_rect.append(image_rect)

        if h < w:
            newH = round(h * 750 / w)
            FnewIm = cv2.resize(image_rect, (750, newH))
        else:
            newW = round(w * 750 / h)
            FnewIm = cv2.resize(image_rect, (newW , 750))

        image_pil = Image.fromarray(FnewIm) # RGBからPILフォーマットへ変換
        image_tk  = ImageTk.PhotoImage(image_pil, master = RT) # ImageTkフォーマットへ変換
        
        images_tk.append(image_tk)
        print(str(filePathP[e]) + ' is appended')

    return images_tk

def goUDLR(event):
    global rect_Up
    global rect_Left
    global canvas
    global newImages
    udlr = event.widget["text"] #openInitialのudlrとは無関係'Up','','Right','Down'

    if udlr == 'Up' and rect_Up > 9:
        rect_Up -= 10
    elif udlr == 'Left' and rect_Left > 9:
        rect_Left -= 10
    elif udlr == 'Right' and rect_Left + 521 < width_list[num]: #rect_Left + 512 < w - 9
        rect_Left += 10
    elif udlr == 'Down' and rect_Up + 521 < height_list[num]: #rect_Up + 512 < h - 9
        rect_Up += 10

    image_bgr = cv2.imread(filePathP[num])
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB) # imreadはBGRなのでRGBに変換
    h, w, _ = image_rgb.shape
    images_rgb.append(image_rgb)

    image_rect = cv2.rectangle(image_rgb,(rect_Left, rect_Up), (rect_Left + 512, rect_Up + 512), (255, 255, 255),10)

    h = height_list[num]
    w = width_list[num]
    if h < w:
        newH = round(h * 750 / w)
        FnewIm = cv2.resize(image_rect, (750, newH))
    else:
        newW = round(w * 750 / h)
        FnewIm = cv2.resize(image_rect, (newW , 750))

    image_pil = Image.fromarray(FnewIm) # RGBからPILフォーマットへ変換
    image_tk  = ImageTk.PhotoImage(image_pil, master = canvas) # ImageTkフォーマットへ変換
    newImages.append(image_tk) # gabage collection で消えるからリストに保存しておく?

    canvas.destroy()
    # imageキャンバス作成
    canvas = tkinter.Canvas(root, bg="#AAAAAA", height=750, width=750)
    # imageキャンバス表示
    canvas.place(x=0, y=0)

    canvas.create_image(0, 0, image=image_tk, anchor='nw',tag='delIm') # ImageTk 画像配置

def trimAndNext():
    global num

    newPicDir = dir_pathP + '/512' + filesP[num]
    image_bgr = cv2.imread(filePathP[num])
    newimage_bgr = image_bgr[rect_Up : rect_Up + 512, rect_Left : rect_Left + 512]

    f = open(newPicDir,'w')
    cv2.imwrite(newPicDir, newimage_bgr, [cv2.IMWRITE_JPEG_QUALITY, 100])
    f.close()

    num += 1
    print(str(num) + ' / ' + str(len(filesP)))

    if num == len(filesP):
        toFinish()
    else:
        canvas.delete('delIm')
        canvas.create_image(0, 0, image=IM[num], anchor='nw',tag='delIm') # ImageTk 画像配置

def through():
    global num
    
    num += 1
    print(str(num) + ' / ' + str(len(filesP)))

    if num == len(filesP):
        toFinish()
    else:
        canvas.delete('delIm')
        canvas.create_image(0, 0, image=IM[num], anchor='nw',tag='delIm') # ImageTk 画像配置

def openInitial():
    global root
    global image_rgb
    global canvas
    global changeCanvas
    global label
    global IM
    global dir_pathImage
    global rect_Up
    global rect_Left

    root = tkinter.Tk()
    root.title(u"ImageAndTagEdit")
    root.geometry("1000x800+50+30")

    # imageキャンバス作成
    canvas = tkinter.Canvas(root, bg="#AAAAAA", height=750, width=750)
    # imageキャンバス表示
    canvas.place(x=0, y=0)

    #dir_pathImage = dirImagesOrTags.dir_PathP
    dir_pathImage = 'C:/Users/Mining-Base/Desktop/EnglishOnlyFileName/picture'
    
    IM = makeImageTKList(dir_pathImage,canvas)
    newImages.append(IM[0])
    rect_Up = 0
    rect_Left = rect_left_list[num]

    canvas.create_image(0, 0, image=newImages[0], anchor='nw',tag='delIm') # ImageTk 画像配置

    # UpDownLRキャンバス作成
    UDLRCanvas = tkinter.Canvas(root, bg="#AABBCC", height=225, width=225)
    # UpDownLRキャンバス表示
    UDLRCanvas.place(x=760, y=0)

    udlr = ['Up','Left','Right','Down']
    #goUDLRのudlrとは無関係

    for i in range(4):
        button_tag = tkinter.Button(UDLRCanvas, text=udlr[i], width=5, height=0, font=("",15,"normal","bold"))
        button_tag.bind("<ButtonPress>", goUDLR)
        button_tag.place(x=70 * (((i + 1) * 2 - 1) % 3) + 10,y=70 * (((i + 1) * 2 - 1) // 3) + 25)

    button_trim = tkinter.Button(root, text="trim", command=trimAndNext, width=0, height=0, font=("",15,"normal","bold"))
    #button_trim.bind("<ButtonPress>", trimAndNext)
    button_trim.place(x=770,y=250)

    button_through = tkinter.Button(root, text="through", command=through, width=0, height=0, font=("",15,"normal","bold"))
    #button_through.bind("<ButtonPress>", through)
    button_through.place(x=850,y=250)

    root.mainloop()