import tkinter
import sys
import importlib

editList = ['finishTest','EachImageTo512','DivideImageToOtheFolder','SlideShow'],[0,2,2,2]

dir = ['E:/DATA/ImageTagChangeForSD/ImageTagChangeForSD/',
        'E:/DATA/ImageTagChangeForSD/ImageTagChangeForSD/ImageAll/',
        'E:/DATA/ImageTagChangeForSD/ImageTagChangeForSD/ImageEach/',
        'E:/DATA/ImageTagChangeForSD/ImageTagChangeForSD/TagAll/',
        'E:/DATA/ImageTagChangeForSD/ImageTagChangeForSD/TagEach/',
        ]

'''
{dirNum}
ImageTagChangeForSD/{0}
    ├--ImageAll{1}
    ├--ImageEach{2}
    ├--TagAll{3}
    └--TagEach{4}
'''

def selectCategory(event):
    selCat = event.widget["text"]
    print(selCat)
    for e,whatEdit in enumerate(editList[0]):
        print(whatEdit)
        if (selCat == whatEdit):
            print('SAME')
            dirNum = editList[1][e]
            WDPath = dir[dirNum]
            print(WDPath)
            sys.path.append(WDPath)

            print(selCat)
            whatPy = importlib.import_module(selCat)

            whatPy.openInitial()

    root.withdraw()

root = tkinter.Tk()
root.title(u"集中編集")
root.geometry("320x225+200+50")

Canvas = tkinter.Canvas(root, bg="#AABBCC", height=205, width=300)
Canvas.place(x=10, y=10)

for i,tag in enumerate(editList[0]):
    print(tag)
    button_tag = tkinter.Button(Canvas, text=editList[0][i], width=0, height=0, font=("",15,"normal","bold"))
    button_tag.bind("<ButtonPress>", selectCategory)
    button_tag.place(x=10,y=50 * i + 10)

root.mainloop()