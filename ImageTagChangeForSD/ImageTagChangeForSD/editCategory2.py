import tkinter
import ImageTagChangeForSD
import dirImagesOrTags

editCategory2 = ['画像を見ながらタグを編集']

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
    root.title('タグを一つずつ')
    root.geometry("320x520+250+100")

    tagCanvas1 = tkinter.Canvas(root, bg="#AABBCC", height=450, width=300)
    tagCanvas1.place(x=10, y=10)

    for i,tag in enumerate(editCategory2):
        button_tag = tkinter.Button(tagCanvas1, text=editCategory2[i], width=0, height=0, font=("",15,"normal","bold"))
        button_tag.bind("<ButtonPress>", selectCategory)
        button_tag.place(x=260 * (i // 13) + 10,y=50 * (i % 13) + 10)

    button_tag = tkinter.Button(root, text='戻る', width=0, height=0, font=("",15,"normal","bold"))
    button_tag.bind("<ButtonPress>", rtrnToStart)
    button_tag.place(x=10,y=470)

    root.mainloop()