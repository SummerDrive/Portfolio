import sys
import tkinter 
import cv2
from PIL import Image, ImageTk
import os
import time
from functools import partial

# ボタンクリック時処理
def eraseTag(event):
    global combinedNewName
    event.widget.config(fg="red")
    redTag = event.widget["text"]

    newName.append(redTag)
    combinedNewName = ', '.join(newName)

    tags_tk[num].remove(redTag)
    
    textBox.delete(0,tkinter.END)
    textBox.insert(0,combinedNewName)
    print(combinedNewName)

def nextPicture():
    global tagCanvas
    global num
    global newName
    global combinedNewName

    #if 'combinedNewName' not in locals():
    #    combinedNewName = 'None!'

    newPicDir = dir_pathP + '/' + str(num).zfill(3) + '#' + combinedNewName + '.jpg'
    newTagDir = dir_pathT + '/' + str(num).zfill(3) + '#' + combinedNewName + '.txt'
    
    os.rename(filePathP[num],newPicDir)

    joined = ', '.join(tags_tk[num])
    f = open(newTagDir,'w')
    f.write(joined)
    f.close()

    os.remove(filePathT[num])

    tagCanvas.destroy()

    num += 1
    
    canvas.delete('delIm')
    canvas.create_image(0, 0, image=images_tk[num], anchor='nw',tag='delIm') # ImageTk 画像配置
    len_tags = len(tags_tk[num])
    print(len_tags)

    # tagキャンバス作成
    tagCanvas = tkinter.Canvas(root, bg="#AABBCC", height=670, width=830)
    # tagキャンバス表示
    tagCanvas.place(x=760, y=0)

    for i,tag in enumerate(tags_tk[num]):
        button_tag = tkinter.Button(tagCanvas, text=tags_tk[num][i], width=20, height=0, font=("",15,"normal","bold"))
        button_tag.bind("<ButtonPress>", eraseTag)
        button_tag.place(x=260 * (i // 13) + 10,y=50 * (i % 13) + 10)

    textBox.delete(0,tkinter.END)
    newName = list()

def open():
    filesP = os.listdir(dir_pathP)
    filesT = os.listdir(dir_pathT)

    root = tkinter.Tk()
    root.title(u"ImageAndTagEdit")
    root.geometry("1600x800+50+30")

    num = 0
    images_tk = []
    tags_tk = []
    newName = []
    filePathP = []
    filePathT = []

    for e,file in enumerate(filesP):
        filePathP.append(dir_pathP + '/' + filesP[e])
        print(filePathP[e])
        image_bgr = cv2.imread(filePathP[e])
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB) # imreadはBGRなのでRGBに変換

        h, w, _ = image_rgb.shape
        if h < w:
            newH = round(h * 750 / w)
            FnewIm = cv2.resize(image_rgb, (750, newH))
        else:
            newW = round(w * 750 / h)
            FnewIm = cv2.resize(image_rgb, (newW , 750))

        image_pil = Image.fromarray(FnewIm) # RGBからPILフォーマットへ変換
        image_tk  = ImageTk.PhotoImage(image_pil) # ImageTkフォーマットへ変換
    
        images_tk.append(image_tk)

        filePathT.append(dir_pathT + '/' + filesT[e])

        f = open(filePathT[e], 'r')
        data = f.read()
        f.close()
        tags = data.split(', ')
        tags_tk.append(tags)
        # imageキャンバス作成
        canvas = tkinter.Canvas(root, bg="#AAAAAA", height=750, width=750)
        # imageキャンバス表示
        canvas.place(x=0, y=0)

        canvas.create_image(0, 0, image=images_tk[num], anchor='nw',tag='delIm') # ImageTk 画像配置
        len_tags = len(tags_tk[0])
        print(len_tags)

    # tagキャンバス作成
    tagCanvas = tkinter.Canvas(root, bg="#AABBCC", height=670, width=830)
    # tagキャンバス表示
    tagCanvas.place(x=760, y=0)

    textBox = tkinter.Entry(width=47, font=("",15,"normal","bold"))
    textBox.place(x=760,y=700)

    for i,tag in enumerate(tags_tk[num]):
        button_tag = tkinter.Button(tagCanvas, text=tags_tk[num][i], width=20, height=0, font=("",15,"normal","bold"))
        button_tag.bind("<ButtonPress>", eraseTag)
        button_tag.place(x=260 * (i // 13) + 10,y=50 * (i % 13) + 10)

    button_next = tkinter.Button(root, text="NEXT", command=nextPicture, width=0, height=0, font=("",15,"normal","bold"))
    button_next.place(x=1220,y=740)

    root.mainloop()