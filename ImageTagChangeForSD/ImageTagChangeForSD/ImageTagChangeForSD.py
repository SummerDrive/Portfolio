import tkinter

import editCategory1
import editCategory2
import editCategory3
import editCategory4

editCategory = ['画像を一つずつ','タグを一つずつ','画像をファイル内一斉','タグをファイル内一斉']

def open():
    # ボタンクリック時処理
    def selectCategory(event):
        selCat = event.widget["text"]

        if (selCat == '画像を一つずつ'):
            root.withdraw()
            editCategory1.open()
        elif (selCat == 'タグを一つずつ'):
            root.withdraw()
            editCategory2.open()
        elif (selCat == '画像をファイル内一斉'):
            root.withdraw()
            editCategory3.open()
        elif (selCat == 'タグをファイル内一斉'):
            root.withdraw()
            editCategory4.open()

    root = tkinter.Tk()
    root.title(u"画像タグ編集　for SD")
    root.geometry("320x225+200+50")

    Canvas = tkinter.Canvas(root, bg="#AABBCC", height=205, width=300)
    Canvas.place(x=10, y=10)

    for i,tag in enumerate(editCategory):
        button_tag = tkinter.Button(Canvas, text=editCategory[i], width=0, height=0, font=("",15,"normal","bold"))
        button_tag.bind("<ButtonPress>", selectCategory)
        button_tag.place(x=10,y=50 * i + 10)

    root.mainloop()
