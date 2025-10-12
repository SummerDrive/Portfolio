import tkinter
import os
import sys
#sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
import importlib
from ImageEach import EachImageTo512,DivideImageToOtheFolder,SlideShow
#from TagEach import TagEditWithLookingImage
from ImageAll import EditTo512,FromImageNameToNumber #,Enlargeimagby3x,FindSameImage,ImageChan-gy,imageresize
#from TagAll import AddTags,EraceTags,FromTagNameToNumber,PrintAllTags
import whatDoList

whDoList = whatDoList.WDL

def selectWhatDo(whDo):
    for i,wh in enumerate(whDoList):
        if whDo == wh[1]:
            print('selectWhatDo(' + whDo + ') = ' + str(i))
            return i

def getBoxPath(WhatEdJ):
    if WhatEdJ == '画像を見ながらタグを編集':
        dir_PathP = box1.get()
        dir_PathP_new = box1new.get()
        dir_PathT = box2.get()
        dir_PathT_new = box2new.get()
    if WhatEdJ in whatDoList.pathP:
        dir_PathP = box1.get()
        dir_PathP_new = box1new.get()        
        dir_PathT = 'None'
        dir_PathT_new = 'None'
    if WhatEdJ in whatDoList.pathT:
        dir_PathP = 'None'
        dir_PathP_new = 'None'
        dir_PathT = box2.get()
        dir_PathT_new = box2new.get()
    return dir_PathP,dir_PathP_new,dir_PathT,dir_PathT_new

def sameOrDivideImagesFolder(event):
    global box1new
    global button_imagesFolder

    txt = event.widget['text']
    if txt == '同一の画像フォルダ':
        box1new['state'] = 'normal'
        button_imagesFolder['text'] = '別々の画像フォルダ'
        button_imagesFolder['bg'] = 'skyblue'
    elif txt == '別々の画像フォルダ':
        box1new['state'] = 'disable'
        button_imagesFolder['text'] = '同一の画像フォルダ'
        button_imagesFolder['bg'] = 'lightgreen'

def sameOrDivideTagsFolder(event):
    global box2new
    global button_tagsFolder

    txt = event.widget['text']
    if txt == '同一のタグフォルダ':
        box2new['state'] = 'normal'
        button_tagsFolder['text'] = '別々のタグフォルダ'
        button_tagsFolder['bg'] = 'skyblue'
    elif txt == '別々のタグフォルダ':
        box2new['state'] = 'disable'
        button_tagsFolder['text'] = '同一のタグフォルダ'
        button_tagsFolder['bg'] = 'lightgreen'

def sameOrDivideTagsFolder(event):
    global box2new
    global button_tagsFolder

    txt = event.widget['text']
    if txt == '同一のタグフォルダ':
        button_tagsFolder['text'] = '別々のタグフォルダ'
        button_tagsFolder['bg'] = 'skyblue'
    elif txt == '別々のタグフォルダ':
        box2new['state'] = 'disable'
        button_tagsFolder['text'] = '同一のタグフォルダ'
        button_tagsFolder['bg'] = 'lightgreen'

def DTON(event):# DeskTopOrNote
    global button_dton

    txt = event.widget['text']
    if txt == 'デスクトップ':
        button_dton['text'] = 'ノートPC'
        button_dton['bg'] = 'lightgreen'
    elif txt == 'ノートPC':
        button_dton['text'] = 'デスクトップ'
        button_dton['bg'] = 'skyblue'

def goToEdit(event):
    global dir_PathP
    global dir_PathP_new
    global dir_PathT
    global dir_PathP_new
    global deskTopOrNote

    num = selectWhatDo(whatEdit)
    
    WDPath = 'E:/DATA/ImageTagChangeForSD/ImageTagChangeForSD/' + whDoList[num][2]
    print(WDPath)
    sys.path.append(WDPath)
    
    global whatPy
    whatPy = importlib.import_module(whDoList[num][0])
    
    root.withdraw()
    
    dir_PathP = getBoxPath(whatEdit)[0]
    dir_PathP_new = getBoxPath(whatEdit)[1]
    dir_PathT = getBoxPath(whatEdit)[2]
    dir_PathT_new = getBoxPath(whatEdit)[3]
    deskTopOrNote = button_dton['text']

    pathes = dir_PathP + ', ' + dir_PathP_new + ', ' + dir_PathT + ', ' + dir_PathT_new
    print(pathes)
    f = open('recordedPath.txt','w')
    f.write(pathes)
    f.close()

    whatPy.openInitial()

def openInitial():
    global whatEdit
    for i in range(len(whDoList)):
        #print("A = " + whDoList[i][1])
        if whatEdit == whDoList[i][1]:
            print("B = " + whDoList[i][0])
    
    f = open('recordedPath.txt','r')
    data = f.read()
    f.close()
    data =data.replace('\\','/')
    recordedPathes = data.split(", ")
    for j,path in enumerate(recordedPathes):
        if path == 'None':
            recordedPathes[j] = ''
    
    global root
    global box1
    global box1new
    global box2
    global box2new
    global button_imagesFolder
    global button_tagsFolder
    global button_dton

    root = tkinter.Tk()
    root.title(whatEdit)
    root.geometry("750x200+250+100")

    label1 = tkinter.Label(root, text="ImagesFolder", width=0, height=0)
    box1 = tkinter.Entry(root, width=100)
    box1.insert(0, recordedPathes[0])
    label1new = tkinter.Label(root, text="NewImagesFolder", width=0, height=0)
    box1new = tkinter.Entry(root, width=100)
    box1new.insert(0, recordedPathes[1])

    label2 = tkinter.Label(root, text="TagsFolder", width=0, height=0)
    box2 = tkinter.Entry(root, width=100)
    box2.insert(0, recordedPathes[2])
    label2new = tkinter.Label(root, text="NewTagsFolder", width=0, height=0)
    box2new = tkinter.Entry(root, width=100)
    box1.insert(0, recordedPathes[3])

    label1.place(x=10,y=10)
    box1.place(x=120,y=10)
    label1new.place(x=10,y=40)
    box1new.place(x=120,y=40)
    label2.place(x=10,y=125)
    box2.place(x=120,y=125)
    label2new.place(x=10,y=165)
    box2new.place(x=120,y=165)

    button_imagesFolder = tkinter.Button(root, text='別々の画像フォルダ', width=0, height=0, font=("",15,"normal","bold"))
    button_imagesFolder['bg'] = 'skyblue'
    button_imagesFolder.place(x=10,y=70)

    button_tagsFolder = tkinter.Button(root, text='別々のタグフォルダ', width=0, height=0, font=("",15,"normal","bold"))
    button_tagsFolder['bg'] = 'skyblue'
    button_tagsFolder.place(x=230,y=70)

    if whatEdit in whatDoList.pathT:
        box1['state'] = 'disable'
        box1new['state'] = 'disable'
        button_imagesFolder['state'] = 'disable'
        button_tagsFolder.bind("<ButtonPress>", sameOrDivideTagsFolder)
    elif whatEdit in whatDoList.pathP:
        box2['state'] = 'disable'
        box2new['state'] = 'disable'
        button_tagsFolder['state'] = 'disable'
        button_imagesFolder.bind("<ButtonPress>", sameOrDivideImagesFolder)

    button_tag = tkinter.Button(root, text='GO', width=0, height=0, font=("",15,"normal","bold"))
    button_tag.bind("<ButtonPress>", goToEdit)
    button_tag.place(x=450,y=70)

    button_dton = tkinter.Button(root, text='デスクトップ', width=12, height=0, font=("",15,"normal","bold"))
    button_dton['bg'] = 'skyblue'
    button_dton.bind("<ButtonPress>", DTON)
    button_dton.place(x=510,y=70)

    root.mainloop()