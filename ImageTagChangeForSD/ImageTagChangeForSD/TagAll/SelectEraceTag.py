import os
import time
import tkinter
import dirImagesOrTags
import sys

eraseTags = []

def eraseTag(event):
    global erseTags
    event.widget.config(fg="red")
    redTag = event.widget["text"]

    eraseTags.append(redTag)

def goToExit(event):
    sys.exit()

def goToErace(event):
    for e,txt in enumerate(txts_list):
        f = open(dir_path + '/' + txt)
        tags = f.read()
        f.close

        tags = tags + ', end'
        print(tags)
        for i,tag in enumerate(eraseTags):
            tag2 = ', ' + tag +','
            print('tag2 = ' + tag2)
            tags = tags.replace(tag2,',')
            print(tags)
        tags = tags.replace(', end','')
        time.sleep(0.5)
        
        f = open(dir_path + '/' + txt,"w")
        f.write(tags)
        f.close()

        print(e + 1)
        time.sleep(0.5)
    
    root2 = tkinter.Tk()
    root2.title('finished')
    root2.geometry("300x50+700+400") # 横幅 x 縦幅 + 横位置 + 縦位置
    root2.lift()

    button_go = tkinter.Button(root2, text='EXIT', width=0, height=0, font=("",15,"normal","bold"))
    button_go.bind("<ButtonPress>", goToExit)
    button_go.place(x=20,y=20)

    root2.mainloop()

def openInitial():
    global txts_list
    global dir_path
    dir_path = dirImagesOrTags.dir_PathT
    #print(txts_list[0])
    #print(type(txts_list[0]))
    txts_list = os.listdir(dir_path)

    allTagTxt = []

    for e,txt in enumerate(txts_list):
        f = open(dir_path + '/' + txt)
        tags = f.read().split(', ')
        f.close()
        
        allTagTxt.extend(tags)
        
        setted = set(allTagTxt)
        allTagTxt = list(setted)
        #print(e,allTagTxt)
        #time.sleep(1)

    sortedAllTagTxt = sorted(allTagTxt)
    print(sortedAllTagTxt)

    root = tkinter.Tk()
    root.title(u"SelectEraceTag")
    root.geometry("1700x880+50+30")

    # tagキャンバス作成
    tagCanvas = tkinter.Canvas(root, bg="#AABBCC", height=810, width=1680)
    # tagキャンバス表示
    tagCanvas.place(x=10, y=10)

    #textBox = tkinter.Entry(width=47, font=("",15,"normal","bold"))
    #textBox.place(x=760,y=700)

    for i,tag in enumerate(sortedAllTagTxt):
        button_tag = tkinter.Button(tagCanvas, text=tag, width=17, height=0, font=("",15,"normal","bold"))
        button_tag.bind("<ButtonPress>", eraseTag)
        button_tag.place(x=210 * (i // 16) + 10,y=50 * (i % 16) + 10)

    button_go = tkinter.Button(root, text='GO', width=0, height=0, font=("",15,"normal","bold"))
    button_go.bind("<ButtonPress>", goToErace)
    button_go.place(x=20,y=830)

    root.mainloop()