# DivideImageToOtheFolder
import sys
import tkinter
from tkinter.constants import ROUND 
import cv2
from PIL import Image, ImageTk
import os
import shutil
import numpy as np
import random
from functools import partial
import winsound
import dirImagesOrTags

num = 0
IM = []

images_rgb = []
images_tk = []
heights =[]
widths = []

filePathP = []

imagetk_list = list()

def DTON(sizeInfo,dton):# DeskTopOrNote
    result = round(sizeInfo * dton)
    return result

def makeImageTKList(path,RT):
    global images_tk
    global filesP

    dir_pathP = path.replace('\\','/')
    filesP = os.listdir(dir_pathP)
    random.shuffle(filesP)
    
    for e,file in enumerate(filesP):
        filePathP.append(dir_pathP + '/' + filesP[e])
        if '.jpg' in filePathP[e] or '.png' in filePathP[e]:
            image_bgr = cv2.imread(filePathP[e])
        else:
            image_bgr = cv2.imread('E:/DATA/ImageTagChangeForSD/ImageTagChangeForSD/ImageEach/NoImage.jpg')

        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB) # imreadはBGRなのでRGBに変換
        images_rgb.append(image_rgb)

        h, w, _ = image_rgb.shape #height=960, width=1809 1809 / 960 = 1.884375
        if h * 1.884375< w:#横長過ぎ(横を1809)
            newH = round(h * DTON(1809,DeskTopOrNote) / w)
            FnewIm = cv2.resize(image_rgb, (DTON(1809,DeskTopOrNote), newH))
        else:#縦長過ぎ（縦を960）
            newW = round(w * DTON(960,DeskTopOrNote) / h)
            FnewIm = cv2.resize(image_rgb, (newW , DTON(960,DeskTopOrNote)))

        image_pil = Image.fromarray(FnewIm) # RGBからPILフォーマットへ変換
        image_tk  = ImageTk.PhotoImage(image_pil, master = RT) # ImageTkフォーマットへ変換
        
        images_tk.append(image_tk)
        heights.append(h)
        widths.append(w)

    return images_tk,heights,widths

def makeSizeInfo(RT,imH,imW):
    global canvas2
    h = DTON(200,DeskTopOrNote)
    w = DTON(200,DeskTopOrNote)
     # imageキャンバス作成
    canvas2 = tkinter.Canvas(RT, bg="#AAAAAA", height=h, width=w)
    # imageキャンバス表示
    canvas2.place(x=DTON(1700,DeskTopOrNote), y=10)#1910 -10 - 200,
    
    rectH = round(imH * DeskTopOrNote / 9.5)
    rectW = round(imW * DeskTopOrNote / 9.5)

    canvas2.create_rectangle(5, 5, 5 + rectW, 5 + rectH, fill = 'green', outline ='#00f')

    labelH = tkinter.Label(canvas2, text=imH, font=("",15,"normal","bold"))
    labelH.place(x=w - 50,y=round(rectH * 0.3))

    labelW = tkinter.Label(canvas2, text=imW, font=("",15,"normal","bold"))
    labelW.place(x=round(rectW * 0.3),y=h - 50)

def nextImage():
    global root
    global after_id
    global num
    global button_stopOrStart
    global label_name
    global canvas2
    global canvas_button

    if button_stopOrStart["text"] == 'STOP':
        num += 1
    elif button_stopOrStart["text"] == 'START':
        button_stopOrStart["text"] = 'STOP'
        label_name.destroy()
        canvas2.destroy()
        canvas_button.destroy()

    if num == len(filesP):
        toFinish()

    else:
        canvas.delete('delIm')
        canvas.create_image(0, 0, image=IM[num], anchor='nw',tag='delIm') # ImageTk 画像配置

        after_id = root.after(10000, nextImage)
        print(num)
        print(dir_pathImage + '/' + filesP[num])

def toFinish():
    finishPath = 'E:/DATA/ImageTagChangeForSD/ImageTagChangeForSD'
    sys.path.append(finishPath)
    import finishTest
    finishTest

def moveImage():
    global num

    shutil.move(filePathP[num], newDir_pathImage)

    num += 1
    print(str(num) + ' / ' + str(len(filesP)))

    if num == len(filesP):
        toFinish()

    else:
        f = open('move.wav', 'rb')
        data = f.read()
        f.close()

        winsound.PlaySound(data, winsound.SND_MEMORY)

        nextImage()

def remainImage():
    global num
    global canvas2

    num += 1
    print(str(num) + ' / ' + str(len(filesP)))

    if num == len(filesP):
        toFinish()

    else:
        f = open('remain.wav', 'rb')
        data = f.read()
        f.close()

        winsound.PlaySound(data, winsound.SND_MEMORY)

        nextImage()

def stopOrStart(event):
    global root
    global after_id
    global button_stopOrStart
    global label_name
    global canvas2
    global canvas_button
    txt = event.widget["text"]
    if txt == 'STOP':
        root.after_cancel(after_id)
        print(after_id)
        button_stopOrStart["text"] = 'START'

        label_name = tkinter.Label(canvas, text=dir_pathImage + '/' + filesP[num], font=("",15,"normal","bold"))
        label_name.place(x=10, y=10)

        makeSizeInfo(root,IM_H[num],IM_W[num])

        canvas_button = tkinter.Canvas(root, bg="#AAAAAA", height=88, width=86)
        canvas_button.place(x=DTON(1817,DeskTopOrNote), y=DTON(820,DeskTopOrNote))

        button_move = tkinter.Button(canvas_button, text="MOVE>>", command=moveImage, width=6, height=0, font=("",15,"normal","bold"))
        button_move.place(x=5,y=5)

        button_remain = tkinter.Button(canvas_button, text="REMAIN", command=remainImage, width=6, height=0, font=("",15,"normal","bold"))
        button_remain.place(x=5,y=47)
    elif txt == 'START':
        root.after(5000, nextImage)
        button_stopOrStart["text"] = 'STOP'
        label_name.destroy()
        canvas2.destroy()
        canvas_button.destroy()

def openInitial():
    global root
    global after_id
    global canvas
    global changeCanvas
    global label
    global IM
    global IM_H
    global IM_W
    global dir_pathImage
    global newDir_pathImage
    global DeskTopOrNote
    global button_stopOrStart

    if dirImagesOrTags.deskTopOrNote == 'デスクトップ':
        DeskTopOrNote = 1
    elif dirImagesOrTags.deskTopOrNote == 'ノートPC':
        DeskTopOrNote = 0.75

    RTHeight = DTON(965,DeskTopOrNote)
    RTWidth = DTON(1910,DeskTopOrNote)

    root = tkinter.Tk()
    root.title(u"ImageColorBrightnessChange")
    root.geometry('{0}x{1}+0+30'.format(RTWidth,RTHeight))#"1910x965+0+30"

    dir_pathImage = dirImagesOrTags.dir_PathP
    newDir_pathImage = dirImagesOrTags.dir_PathP_new

    print(makeImageTKList(dir_pathImage,root)[1])
    IM = makeImageTKList(dir_pathImage,root)[0]
    IM_H = makeImageTKList(dir_pathImage,root)[1]
    IM_W = makeImageTKList(dir_pathImage,root)[2]

    # imageキャンバス作成
    canvas = tkinter.Canvas(root, bg="#AAAAAA", height=DTON(960,DeskTopOrNote), width=DTON(1809,DeskTopOrNote))
    # imageキャンバス表示
    canvas.place(x=2, y=0)
    
    canvas.create_image(0, 0, image=IM[num], anchor='nw', tag='delIm') # ImageTk 画像配置

    button_stopOrStart = tkinter.Button(root, text="STOP", width=6, height=0, font=("",15,"normal","bold"))
    button_stopOrStart.bind("<ButtonPress>", stopOrStart)
    button_stopOrStart.place(x=DTON(1822,DeskTopOrNote), y=DTON(917,DeskTopOrNote))

    after_id = root.after(5000, nextImage)

    root.mainloop()