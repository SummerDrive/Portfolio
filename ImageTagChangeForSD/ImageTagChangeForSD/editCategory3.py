import tkinter
import ImageTagChangeForSD
import dirImagesOrTags

editCategory3 = ['画像を512＊512に切り取る','画像名を連番に','周囲を黒,縦横３倍','同一画像を抽出','B,R,O,P,C,Yで色選択','サイズ変更']

def selectCategory(event):
    selCat = event.widget["text"]

    dirImagesOrTags.whatEdit = selCat
    root.withdraw()
    dirImagesOrTags.openInitial()

def rtrnToStart(event):
    root.withdraw()
    ImageTagChangeForSD.open()

def open():
    global root
    root = tkinter.Tk()
    root.title('画像をファイル内一斉')
    root.geometry("320x520+250+100")

    tagCanvas1 = tkinter.Canvas(root, bg="#AABBCC", height=450, width=300)
    tagCanvas1.place(x=10, y=10)

    for i,tag in enumerate(editCategory3):
        button_tag = tkinter.Button(tagCanvas1, text=editCategory3[i], width=0, height=0, font=("",15,"normal","bold"))
        button_tag.bind("<ButtonPress>", selectCategory)
        button_tag.place(x=260 * (i // 13) + 10,y=50 * (i % 13) + 10)

    button_tag = tkinter.Button(root, text='戻る', width=0, height=0, font=("",15,"normal","bold"))
    button_tag.bind("<ButtonPress>", rtrnToStart)
    button_tag.place(x=10,y=470)

    root.mainloop()