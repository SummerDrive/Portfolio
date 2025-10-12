import sys
import tkinter 
import cv2
from PIL import Image, ImageTk
import os
import numpy as np
from functools import partial
import dirImagesOrTags

num = 0
IM = []
'''
bright = 0
red = 0
green = 0
blue = 0
'''

images_rgb = []
images_tk = []

filePathP = []

imagetk_list = list()

def makeImageTKList(path,RT):
    global images_tk
    global filesP
    dir_pathP = path.replace('\\','/')

    filesP = os.listdir(dir_pathP)

    print(len(filesP))
    for e,file in enumerate(filesP):
        filePathP.append(dir_pathP + '/' + filesP[e])

        image_bgr = cv2.imread(filePathP[e])
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB) # imreadはBGRなのでRGBに変換
        images_rgb.append(image_rgb)

        h, w, _ = image_rgb.shape
        if h < w:
            newH = round(h * 750 / w)
            FnewIm = cv2.resize(image_rgb, (750, newH))
        else:
            newW = round(w * 750 / h)
            FnewIm = cv2.resize(image_rgb, (newW , 750))

        image_pil = Image.fromarray(FnewIm) # RGBからPILフォーマットへ変換
        image_tk  = ImageTk.PhotoImage(image_pil, master = RT) # ImageTkフォーマットへ変換
        
        images_tk.append(image_tk)
        print(str(filePathP[e]) + ' is appended')

    return images_tk

def lutMake(col,fig):
    gam = 1.5 ** fig
    # ルックアップテーブルの生成(ガンマ補正)
    look_up_table = np.zeros((256,1),dtype=np.uint8)
    for i in range(256):
        look_up_table[i][0] = (i/255)**(1.0/gam)*255

    lut = cv2.LUT(col, look_up_table)
    return lut

def colorChange(img):    
    r, g, b = cv2.split(img)  # B(青),G(緑),R(赤)チャンネルごとに分割
    
    r_lut =lutMake(r,labelFigs[0])
    g_lut =lutMake(g,labelFigs[1])
    b_lut =lutMake(b,labelFigs[2])

    img_merge = cv2.merge([r_lut, g_lut, b_lut])

    return img_merge
'''
ボタンクリック時処理
0:Bright - / 4:Bright +
1:red    - / 5:red    +
2:green  - / 6:green  +
3:blue   - / 7:blue   +
'''
color1 = {1:"Brightness", 2:"Red", 3:"Green", 4:"Blue",5:"+"}

labelFigs = [0,0,0]

def changeImage(event):
    global canvas
    global label
    global imagetk_list
    global newImage_rgb
    tag = int(event.widget.tag)
    
    color = tag % 4
    PorM = (tag // 4) * 2 - 1
    
    if color == 0:
        for i in range(3):
            labelFigs[i] += PorM
    else:
        labelFigs[color - 1] += PorM

    newImage_rgb = colorChange(images_rgb[num])

    h, w, _ = newImage_rgb.shape
    if h < w:
        newH = round(h * 750 / w)
        FnewIm = cv2.resize(newImage_rgb, (750, newH))
    else:
        newW = round(w * 750 / h)
        FnewIm = cv2.resize(newImage_rgb, (newW , 750))
    
    image_pilNew = Image.fromarray(FnewIm) # RGBからPILフォーマットへ変換
    image_tkNew  = ImageTk.PhotoImage(image_pilNew, master = root) # ImageTkフォーマットへ変換
    imagetk_list.append(image_tkNew) # gabage collection で消えるからリストに保存しておく?
    
    canvas.destroy
    # imageキャンバス作成
    canvas = tkinter.Canvas(root, bg="#AAAAAA", height=750, width=750)
    # imageキャンバス表示
    canvas.place(x=0, y=0)

    canvas.create_image(0, 0, image=image_tkNew, anchor='nw',tag='delIm') # ImageTk 画像配置

    label.destroy()
    for j in range(3):
        label = tkinter.Label(changeCanvas, text=labelFigs[j], width=5, height=0, font=("",15,"normal","bold"))
        label.place(x=170, y=50 * j + 65)

def nextPicture():
    global num
    global labelFigs
    global label

    if labelFigs != [0,0,0]:
        newPicDir = dir_pathImage + '/#' + str(num).zfill(3) + '#' + filesP[num]
        newimage_bgr = cv2.cvtColor(newImage_rgb, cv2.COLOR_RGB2BGR)

        f = open(newPicDir,'w')
        cv2.imwrite(newPicDir, newimage_bgr, [cv2.IMWRITE_JPEG_QUALITY, 100])
        f.close()

    num += 1
    print(str(num) + ' / ' + str(len(filesP)))

    if num == len(filesP):
        root2 = tkinter.Tk()
        root2.title('finished')
        root2.geometry("300x50+700+400") # 横幅 x 縦幅 + 横位置 + 縦位置

    else:
        labelFigs = [0,0,0]
        
        canvas.delete('delIm')
        canvas.create_image(0, 0, image=IM[num], anchor='nw',tag='delIm') # ImageTk 画像配置
        
        label.destroy
        for j in range(3):
            label = tkinter.Label(changeCanvas, text=labelFigs[j], width=5, height=0, font=("",15,"normal","bold"))
            label.place(x=170, y=50 * j + 65)

def openInitial():
    global root
    global canvas
    global changeCanvas
    global label
    global IM
    global dir_pathImage

    root = tkinter.Tk()
    root.title(u"ImageColorBrightnessChange")
    root.geometry("1180x800+50+30")

    dir_pathImage = dirImagesOrTags.dir_PathP
    IM = makeImageTKList(dir_pathImage,root)
    
    # imageキャンバス作成
    canvas = tkinter.Canvas(root, bg="#AAAAAA", height=750, width=750)
    # imageキャンバス表示
    canvas.place(x=0, y=0)
    
    canvas.create_image(0, 0, image=IM[num], anchor='nw', tag='delIm') # ImageTk 画像配置

    # buttonキャンバス作成
    changeCanvas = tkinter.Canvas(root, bg="#AABBCC", height=670, width=405)
    # buttonキャンバス表示
    changeCanvas.place(x=760, y=0)

    for i in range(8):
        if i < 4:
            PlusOrMinus = '-'
        else:
            PlusOrMinus = '+'

        colorNum = i % 4 + 1

        if colorNum in color1:
            brgb = color1[colorNum]

        txt = brgb + ' ' + PlusOrMinus
        button_change = tkinter.Button(changeCanvas, text=txt, width=10, height=0, font=("",15,"normal","bold"))
        button_change.bind("<ButtonPress>", changeImage)
        button_change.tag = str(i)
        button_change.place(x=260 * (i // 4) + 10,y=50 * (i % 4) + 10)

    for j in range(3):
        label = tkinter.Label(changeCanvas, text=labelFigs[j], width=5, height=0, font=("",15,"normal","bold"))
        label.place(x=170, y=50 * j + 65)

    button_next = tkinter.Button(root, text="NEXT", command=nextPicture, width=0, height=0, font=("",15,"normal","bold"))
    button_next.place(x=1090,y=740)

    root.mainloop()